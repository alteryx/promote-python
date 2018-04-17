import requests
import base64
import os
import sys
import logging
import json
import pprint as pp
import urllib
import re
import tempfile
import tarfile

from . import utils
from .metadata import Metadata

class Promote(object):
    """
    Promote allows you to interact with the Promote API.

    Parameters
    ==========
    username: str
        Your Promote username
    apikey: str
        Your Promote APIKEY
    url: str
        URL of your promote server. i.e. https://promote.acmecorp.com/, http://10.252.2.10/

    Examples
    ========
    >>> p = promote.Promote("colin", "789asdf879h789a79f79sf79s", "https://my-promote.mycompany.com/")
    >>> p.deploy("HelloModel", promoteModel, testdata=testdata, confirm=True, dry_run=False, verbose=0)
    >>> p.predict("HelloWorld", { "name": "Colin" })
    """

    def __init__(self, username, apikey, url):
        if username is None:
            raise Exception("Specify a username")

        if apikey is None:
            raise Exception("Specify a apikey")

        if url is None:
            raise Exception("Specify a url")

        self.username = username
        self.apikey = apikey
        self.url = url

        self.addedfiles = []

        self.metadata = Metadata()
        self.deployment_file = os.path.realpath(sys.argv[0])
        if not os.path.exists(self.deployment_file):
            raise Exception('The path to your deployment file does not exist: {}'.format(
                self.deployment_file))
        self.deployment_dir = os.path.dirname(self.deployment_file)
        if not os.path.exists(self.deployment_dir):
            raise Exception('The path to your deployment directory does not exist: {}'.format(
                self.deployment_dir))

    def _get_function_source_code(self, functionToDeploy):
        source = ''
        with open(self.deployment_file, 'r', encoding='utf-8') as f:
            source = f.read()

        source += "\npromoteModel = {}\n".format(functionToDeploy.__name__)

        return source

    def _get_objects(self):
        objects_dir = os.path.join(self.deployment_dir, 'objects')

        if not os.path.exists(self.deployment_dir):
            raise Exception('The path to your deployment directory does not exist: {}'.format(
                self.deployment_dir))

        if not os.path.exists(objects_dir):
            logging.info('no pickles directory found in {}'.format(objects_dir))
            # Create an empty tarfile if there is no objects directory
            tarName = os.path.join(self.deployment_dir, 'objects.tar.gz')
            tarFile = open(tarName, 'wb')
            with tarfile.open(mode='w:gz', fileobj=tarFile) as tar:
                pass
            tarFile.close()
            return {}, tarName

        tarName = os.path.join(objects_dir, 'objects.tar.gz')
        if os.path.exists(tarName):
            os.unlink(tarName)

        objects = {}
        for path in os.listdir(objects_dir):
            fullpath = os.path.join(objects_dir, path)
            if os.path.isdir(fullpath):
                self.addedfiles.append(path)
                objects[path] = path
            else:
                self.addedfiles.append(path)
                objects[path] = path

        tarFile = open(tarName, 'wb')
        with tarfile.open(mode='w:gz', fileobj=tarFile) as tar:
            tar.add(objects_dir, arcname='objects')
        tarFile.close()

        return objects, tarName

    def _get_requirements(self):
        requirements_file = os.path.join(
            self.deployment_dir, 'requirements.txt')
        if not os.path.exists(requirements_file):
            logging.info(
                'no requirements file found in {}'.format(requirements_file))
            raise Exception(
                "You don't have a requirements.txt file. It's impossible to deploy a model without it")

        with open(requirements_file, 'r') as f:
            requirements = f.read()
            if "promote" not in requirements:
                raise Exception(
                    "You don't have Promote listed as a requirement. It's impossible to deploy a model without it")
        return requirements

    def _get_promotesh(self):
        promotesh_file = os.path.join(self.deployment_dir, 'promote.sh')
        if not os.path.exists(promotesh_file):
            logging.info('no promote.sh file found in {}'.format(promotesh_file))
            return {}

        with open(promotesh_file, 'r') as f:
            promote_file_obj = f.read()
        return promote_file_obj

    def _get_helper_modules(self):
        helpers_dir = os.path.join(self.deployment_dir, 'helpers')
        if not os.path.exists(helpers_dir):
            logging.info(
                'helpers directory does not exist: {}'.format(helpers_dir))
            return []

        helpers = [
            dict(name='__init__.py', parent_dir='helpers', source='')
        ]
        for filename in os.listdir(helpers_dir):
            self.addedfiles.append(filename)
            helper_file = os.path.join(helpers_dir, filename)

            if not os.path.isfile(helper_file) or helper_file.endswith('.pyc'):
                continue

            with open(helper_file, 'rb') as fh:
                logging.info('appending file {}'.format(filename))
                source = fh.read().decode('utf-8')
                helpers.append(dict(
                    name=filename,
                    parent_dir='helpers',
                    source=source
                ))
        return json.dumps(helpers)

    def _get_bundle(self, functionToDeploy, modelName):
        bundle = dict(
            modelname = modelName,
            language = "python",
            username = self.username,
            code = None,
            objects = {},
            modules = [],
            image = None,
            reqs = "",
            promotesh = "",
            metadata = {}
        )

        logging.info('deploying model using file: {}'.format(
            self.deployment_file))

        # extract source code for function
        bundle['code'] = self._get_function_source_code(functionToDeploy)
        bundle['reqs'] = self._get_requirements()
        bundle['promotesh'] = self._get_promotesh()
        bundle['modules'] = self._get_helper_modules()

        return bundle

    def _confirm(self):
        response = input(
            "Are you sure you'd like to deploy this model? (y/N): ")
        if response.lower() != "y":
            logging.warning("Deployment Cancelled")
            sys.exit(1)

    def _upload_deployment(self, bundle, modelObjectsPath):
        deployment_url = urllib.parse.urljoin(self.url, '/api/deploy/python')
        return utils.post_file(deployment_url, (self.username, self.apikey), bundle, modelObjectsPath)

    def deploy(self, modelName, functionToDeploy, testdata, confirm=False, dry_run=False, verbose=1):
        """
        Deploys a model to your Promote instance. If it's the first time the model is being deployed,
        a new endpoint will be created for the model.

        Parameters
        ==========
        modelName: str
            Name of the model you're deploying. This will be the name of the endpoint for the model as well.
        functionToDeploy: func
            Function you'd like to deploy to Promote.
        testdata: dict, list
            Sample data that will be used to validate your model can successfully execute.
        confirm: bool (default: False)
            If True, deployment will pause before uploading to the server and validate that you actually want
            to deploy.
        dry_run: bool (default: False)
            If True, deployment will exit prior to uploading to the server and will instead return the bundle.
        verbose: int (default: 0; 0-2)
            Controls the amount of logs displayed. Higher values indiciate more will be shown.

        Examples
        ========
        >>> def sayHello(data):
        ...     return "Hello " + str(data)
        >>> p.deploy("HelloModel", sayHello, testdata=testdata, confirm=True, dry_run=False, verbose=0)
        """
        levels = {
            0: logging.WARNING,
            1: logging.INFO,
            2: logging.DEBUG,
        }
        logging.basicConfig(
            format='[%(levelname)s]: %(message)s',
            level=levels.get(verbose, logging.WARNING)
        )

        if os.environ.get('PROMOTE_PRODUCTION'):
            return

        if re.match("^[A-Za-z0-9]+$", modelName) == None:
            logging.warning(
                "Model name can only contain following characters: A-Za-z0-9")
            return

        if len(modelName) > 35:
            logging.warning("Model name must be fewer than 35 characters")
            return

        bundle = self._get_bundle(functionToDeploy, modelName)
        modelObjects, tarfilePath = self._get_objects()
        bundle['objects'] = modelObjects
        if len(self.metadata) > 6:
            raise Exception('Attempted to deploy with {} metadata items. Max allowed is 6.'.format(len(bundle['metadata'])))
        bundle['metadata'] = json.dumps(self.metadata)

        if confirm == True:
            self._confirm()

        logging.info('Deploying with the following files:')
        for f in self.addedfiles:
            logging.info(f)

        if dry_run == True:
            logging.warning('dry_run=True, not deploying model')
            return bundle

        response = self._upload_deployment(bundle, tarfilePath)

        return response

    def predict(self, modelName, data, username=None):
        """
        Makes a prediction using the model's endpoint on your Promote server.
        You can query a different user's model by passing a username.

        Parameters
        ==========
        modelName: str
            Name of the model you'd like to query
        data: dict, list
            Data you'd like to send to the model to be scored.
        username: str
            Username of the model you'd like to query. This will default to the one set in the Promote constructor.
            However if you'd like to query another person's model or a production model, this will come in handy.

        Examples
        ========
        >>> p = Promote("tom", "4b48cfdecd0841c1b85a806d3add5b11", "https://my-promote.mycompany.com/")
        >>> p.predict("HelloWorld", { "name": "Billy Bob Thorton" })
        # uses billybob's HelloWorld
        >>> p.predict("HelloWorld", { "name": "Billy Bob Thorton" }, username="billybob")
        """
        prediction_url = urllib.parse.urljoin(self.url, os.path.join(
            self.username, 'models', modelName, 'predict'))
        username = username if username else self.username

        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(
            url=prediction_url,
            headers=headers,
            json=data,
            auth=(self.username, self.apikey)
        )
        return response.json()
