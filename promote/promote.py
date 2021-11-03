import requests
import os
import sys
import logging
import json
import urllib
import re
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
    >>> p.deploy("HelloModel", promoteModel, test_data=testdata, confirm=True, dry_run=False, verbose=0)
    >>> p.predict("HelloWorld", { "name": "Colin" })
    """

    def __init__(self, username: str = None, apikey: str = None, url: str = None) -> None:
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

    def _get_function_source_code(self, function_to_deploy: str) -> str:
        source = ''
        with open(self.deployment_file, 'r', encoding='utf-8') as f:
            source = f.read()

        source += "\npromoteModel = {}\n".format(function_to_deploy.__name__)
        return source

    def _get_objects(self) -> (dict, str):
        objects_dir = os.path.join(self.deployment_dir, 'objects')

        if not os.path.exists(self.deployment_dir):
            raise Exception('The path to your deployment directory does not exist: {}'.format(
                self.deployment_dir))

        if not os.path.exists(objects_dir):
            logging.info('no pickles directory found in {}'.format(objects_dir))
            # Create an empty tarfile if there is no objects directory
            tar_name = os.path.join(self.deployment_dir, 'objects.tar.gz')
            with open(tar_name, 'wb') as tar_file, tarfile.open(mode='w:gz', fileobj=tar_file) as tar:
                pass
            return {}, tar_name

        tar_name = os.path.join(objects_dir, 'objects.tar.gz')
        if os.path.exists(tar_name):
            os.unlink(tar_name)

        objects = {}
        for path in os.listdir(objects_dir):
            fullpath = os.path.join(objects_dir, path)
            if os.path.isdir(fullpath):
                self.addedfiles.append(path)
                objects[path] = path
            else:
                self.addedfiles.append(path)
                objects[path] = path

        with open(tar_name, 'wb') as tar_file, tarfile.open(mode='w:gz', fileobj=tar_file) as tar:
            tar.add(objects_dir, arcname='objects')

        return objects, tar_name

    def _get_requirements(self) -> str:
        requirements_file = os.path.join(self.deployment_dir, 'requirements.txt')
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

    def _get_promote_sh(self) -> str:
        promote_sh_file = os.path.join(self.deployment_dir, 'promote.sh')
        if not os.path.exists(promote_sh_file):
            logging.info('no promote.sh file found in {}'.format(promote_sh_file))
            return {}

        with open(promote_sh_file, 'r') as f:
            promote_file_obj = f.read()
        return promote_file_obj

    def _get_helper_modules(self) -> str:
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

    def _get_bundle(self, function_to_deploy: str, model_name: str) -> dict:
        logging.info('deploying model using file: {}'.format(
            self.deployment_file))
        return dict(
           modelname=model_name,
           language="python",
           username=self.username,
           code=self._get_function_source_code(function_to_deploy),
           objects={},
           modules=self._get_helper_modules(),
           image=None,
           reqs=self._get_requirements(),
           promotesh=self._get_promote_sh(),
           metadata={}
        )

    @staticmethod
    def _confirm() -> None:
        response = input(
            "Are you sure you'd like to deploy this model? (y/N): ")
        if response.lower() != "y":
            logging.warning("Deployment Cancelled")
            sys.exit(1)

    def _upload_deployment(self, bundle: dict, model_objects_path: str):
        deployment_url = urllib.parse.urljoin(self.url, '/api/deploy/python')
        return utils.post_file(deployment_url, (self.username, self.apikey), bundle, model_objects_path)

    def deploy(self, model_name: str, function_to_deploy: str, test_data: dict,
               confirm: bool = False, dry_run: bool = False, verbose: int = 1):
        """
        Deploys a model to your Promote instance. If it's the first time the model is being deployed,
        a new endpoint will be created for the model.

        Parameters
        ==========
        model_name: str
            Name of the model you're deploying. This will be the name of the endpoint for the model as well.
        function_to_deploy: func
            Function you'd like to deploy to Promote.
        test_data: dict, list
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
        >>> p.deploy("HelloModel", sayHello, test_data=testdata, confirm=True, dry_run=False, verbose=0)
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

        if re.match("^[A-Za-z0-9]+$", model_name) == None:
            logging.warning(
                "Model name can only contain following characters: A-Za-z0-9")
            return

        if len(model_name) > 35:
            logging.warning("Model name must be fewer than 35 characters")
            return

        bundle = self._get_bundle(function_to_deploy, model_name)
        model_objects, tar_file_path = self._get_objects()
        bundle['objects'] = model_objects
        if len(self.metadata) > 6:
            raise Exception('Attempted to deploy with {} metadata items. Max allowed is 6.'.format(len(bundle['metadata'])))
        bundle['metadata'] = json.dumps(self.metadata)

        if confirm is True:
            self._confirm()

        logging.info('Deploying with the following files:')
        for f in self.addedfiles:
            logging.info(f)

        if dry_run is True:
            logging.warning('dry_run=True, not deploying model')
            return bundle

        response = self._upload_deployment(bundle, tar_file_path)

        return response

    def predict(self, model_name: str, data: dict, username: str = None) -> dict:
        """
        Makes a prediction using the model's endpoint on your Promote server.
        You can query a different user's model by passing a username.

        Parameters
        ==========
        model_name: str
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
            self.username, 'models', model_name, 'predict'))
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
