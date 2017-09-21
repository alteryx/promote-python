import requests
import base64
import os
import sys
import logging
import json
import pprint as pp
import urllib

from . import utils


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
    >>> p = promote.Promote("colin", "789asdf879h789a79f79sf79s", "https://sandbox.c.yhat.com/")
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

        self.deployment_file = os.path.realpath(sys.argv[0])
        if not os.path.exists(self.deployment_file):
            raise Exception('The path to your deployment file does not exist: {}'.format(self.deployment_file))

        self.deployment_dir = os.path.dirname(self.deployment_file)
        if not os.path.exists(self.deployment_dir):
            raise Exception('The path to your deployment directory does not exist: {}'.format(self.deployment_dir))


    def _get_function_source_code(self):
        source = ''
        with open(self.deployment_file, 'r') as f:
            source = f.read()

        # TODO: talk to Colin about this
        if 'def promoteModel(' not in source:
            msg = 'Your model needs to implement the `promoteModel`'
            msg += ' function. Function definition does not appear in {}'
            raise Exception(msg.format(self.deployment_file))
        return source
    
    def _get_objects(self):
        pickle_dir = os.path.join(self.deployment_dir, 'pickles')
        if not os.path.exists(pickle_dir):
            logging.info('no pickles directory found in {}'.format(pickle_dir))
            return {}
        
        objects = {}
        for f in os.listdir(pickle_dir):
            with open(os.path.join(pickle_dir, f), 'rb') as fh:
                obj = fh.read()
                obj = base64.encodebytes(obj).decode('utf-8')
                objects[f] = obj

        return objects

    def _get_requirements(self):
        requirements_file = os.path.join(self.deployment_dir, 'requirements.txt')
        if not os.path.exists(requirements_file):
            logging.info('no requirements file found in {}'.format(requirements_file))
            raise Exception("You don't have a requirements.txt file. It's impossible to deploy a model without it")
        
        with open(requirements_file, 'r') as f:
            requirements = f.read()
            if "promote" not in requirements:
                raise Exception("You don't have Promote listed as a requirement. It's impossible to deploy a model without it")
        return requirements

    def _get_helper_modules(self):
        helpers_dir = os.path.join(self.deployment_dir, 'helpers')
        if not os.path.exists(helpers_dir):
            logging.info('helpers directory does not exist: {}'.format(helpers_dir))
            return []

        helpers = [
            dict(name='__init__.py', parent_dir='helpers', source='')
        ]
        for filename in os.listdir(helpers_dir):
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
        return helpers

    def _get_bundle(self, modelName):
        bundle = dict(
            modelname=modelName,
            language="python",
            username=self.username,
            # below are the things we need to grab
            code=None,
            objects={},
            modules=[],
            image=None, # do we need this anymore?,
            reqs="",
        )

        logging.info('deploying model using file: {}'.format(self.deployment_file))

        # extract source code for function
        bundle['code'] = self._get_function_source_code()
        # get pickles
        bundle['objects'] = self._get_objects()
        bundle['reqs'] = self._get_requirements()
        bundle['modules'] = self._get_helper_modules()

        return bundle

    def _confirm(self):
        response = raw_input("Are you sure you'd like to deploy this model? (y/N): ")
        if response.lower() != "y":
            sys.exit(1)

    def _upload_deployment(self, bundle):
        # TODO: correct this
        deployment_url = urllib.parse.urljoin(self.url, '/api/deploy/python')
        bundle = json.dumps(bundle)
        return utils.post_file(deployment_url, (self.username, self.apikey), bundle)

    def deploy(self, modelName, testdata, confirm=False, dry_run=False, verbose=0):
        """
        Deploys a model to your Promote instance. If it's the first time the model is being deployed, 
        a new endpoint will be created for the model.

        Parameters
        ==========
        modelName: str
            Name of the model you're deploying. This will be the name of the endpoint for the model as well.
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
        >>> p.deploy("HelloModel", testdata=testdata, confirm=True, dry_run=False, verbose=0)
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

        bundle = self._get_bundle(modelName)

        if confirm==True:
            self._confirm()
        
        logging.debug(bundle)
        if dry_run==True:
            return bundle

        response = self._upload_deployment(bundle)
        
        # TODO: maybe not return the raw response (?)
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
        # TODO: correct this
        prediction_url = urllib.parse.urljoin(self.url, os.path.join(self.username, 'model', modelName))
        username = username if username else self.username

        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(
            url=prediction_url,
            headers=headers,
            data=data,
            auth=(self.username, self.apikey)
        )
        return response.json()
    
