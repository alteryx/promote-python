# Alteryx Promote Python Client
Library for deploying Python models to Alteryx Promote.

## Examples
[Hello World](examples/hello-world) - a very simple model

[Hello Vectorized](examples/hello-vectorized) - a vectorized version of the 'Hello World' model

[Iris Classifier](examples/iris-classifier) - use a Support Vector Classifier to predict flower types

[Article Summarizer](examples/article-summarizer) - send a url with a news article and get a summary

[DB Lookup](examples/db-lookup) - lookup a value in a database

[Ensemble Model](examples/ensemble-model) - build and deploy an ensemble model

[Naivebayes Pomegranate](examples/naivebayes-pomegranate) - an Naive Bayes model using the pomegranate library

[Weather Model](examples/weather-model) - send Lat/Lon data and get real-time weather data and classify temperature

## Installation
### Client
To install the promote library, execute the following code from a terminal session:
```shell
pip install promote
```

Please refer to the [promote-r-client](https://github.com/alteryx/promote-r-client) library for instructions on installing the R Client.

### App
Please refer to the [installation guide](https://help.alteryx.com/promote/current/Administer/Installation.htm?tocpath=Administer%7C_____2) for instructions on installing the Promote App.

## Usage
### <a name="directory"></a>Model Directory Structure
```
example-model/
├── deploy.py
├── requirements.txt
├── promote.sh (optional)
├── helpers (optional)
│   ├── __init__.py
│   └── helper_funs.py
└── objects (optional)
    └── my_model.p
```

- [`deploy.py`](#deploypy): our primary model deployment script

- [`requirements.txt`](#requirementstxt): this file tells Promote which libraries to install as dependencies for the model

- [`promote.sh`](#promotesh): this file is executed before your model is built. It can be used to install low-level system packages such as Linux packages

- [`helpers`](#helpers): use this directory to store helper scripts that can be imported by the main deployment script. This is helpful for keeping you deployment script code clean.

- [`objects`](#objects): use this directory to store model, data, and other artifacts that must be loaded into memory when the model is deployed
<hr>

### `deploy.py`
#### Steps:
- [Initial Setup](#setup)
- [Model Function](#modelpredict)
- [@promote.validate_json](#validate)
- [Test Data](#testing)
- [promote.Promote](#promotepromote)
- [Promote.metadata](#promotemetadata)
- [Promote.deploy](#promotedeploy)
- [Promote.predict](#promotepredict)
<hr>

### <a name="setup"></a>Initial Setup
Load the `promote` library that was previously installed:
```python
import promote

# import pickle to deserialize your model
import pickle

# import json to parse your test data
import json
```

Import your saved model object:
```python
# Previously saved model 'pickle.dump( my_model, open( "./objects/my_model.p", "wb" ) )'
my_model = pickle.load( open( "./objects/my_model.p", "rb" ) )
```
<hr>

### <a name="modelpredict"></a>Model Function
The model function is used to define the API endpoint for a model and is executed each time a model is called. **This is the core of the API endpoint.**

**Usage**

`foo(data)`

**Arguments**
- `data`(_list_ or _dict_): the parsed JSON sent to the deployed model

**Example:**
```python
def modelFunction(data):
    my_model.predict(data)
```
<hr>

### <a name="validate"></a>`@promote.validate_json()`
It is possible to decorate your model function with the `promote.validate_json` decorator. This validates that the input data to the model meets specific predefined criteria. Failure to meet these criteria will throw an error.

**Usage**

`@promote.validate_json(aSchema)`

**Arguments**
- `aSchema`(_Schema_): a valid `schema.Schema` object

**Example:**
```python
from schema import Schema, And

@promote.validate_json(Schema({'X1': And(int, lambda s: min([t > 0 for t in s]))},{'X2': And(int, lambda s: min([t > 0 for t in s]))}))
def modelFunction(data):
    my_model.predict(data)
```
<hr>

### <a name="testing"></a>Test Data
It is a good practice to test the model function as part of the deployment script to make sure it successfully produces an output. Once deployed, the `data` being input into the model function will always be in the form of a python [dict](https://docs.python.org/3/tutorial/datastructures.html#dictionaries) or [list](https://docs.python.org/3/tutorial/datastructures.html#more-on-lists). The incoming JSON string will be parsed using the `loads()` method available from the [json](https://docs.python.org/3/library/json.html) library.

**Example:**
```python
testdata = '{"X1":[1,2,3],"X2":[4,5,6]}'
modelFunction(json.loads(testdata))

```
<hr>

### `promote.Promote()`
To deploy models, you'll need to add your username, API key, and URL of Promote to a new instance of the class `Promote`.

**Usage**

`promote.Promote(username, apikey, url)`

**Arguments**
- `username`(_string_): Your Promote username
- `apikey`(_string_): Your Promote APIKEY
- `url`(_string_): URL of your promote server

**Example:**
```python
p = promote.Promote("username", "apikey", "http://promote.company.com/")
```
<hr>

### `Promote.metadata`
Store custom metadata about a model version when it is deployed to the Promote servers. (limited to 6 key-value pairs).

**Arguments**
- `key`(_string_): the name of your metadata (limit 20 characters)
- `value`: a value for your metadata (will be converted to string and limited to 50 characters)

**Example:**
```python
p.metadata.one = 1
p.metadata["two"] = 2
p.metadata['three'] = "this is the third item"
p.metadata.array = [0, 1, 'two']
p.metadata.dict = {'a': 1, 'b': 'two'}
```
<hr>

### `Promote.deploy()`
The deploy function captures the model function, any objects in the `helpers` and `objects` directories, the `requirements.txt` file, and the `promote.sh` file, and sends them in a bundle to the Promote servers.

**Usage**

 `p.deploy(modelName, functionToDeploy, testdata, confirm=False, dry_run=False, verbose=1)`

**Arguments**
- `modelName`(_string_): Name of the model you're deploying (this will be the name of the endpoint for the model as well)
- `functionToDeploy`(_function_): Function you'd like to deploy to Promote
- `testdata`(_list_ or _dict_): Sample data that will be used to validate your model can successfully execute
- `confirm`(_boolean_, optional): If True, deployment will pause before uploading to the server and validate that you actually want to deploy
- `dry_run`(_boolean_, optional): If True, deployment will exit prior to uploading to the server and will instead return the bundle
- `verbose`(_int_, optional): Controls the amount of logs displayed. Higher values indicate more will be shown

**Example:**
```python
p.deploy("MyFirstPythonModel", modelFunction, testdata, confirm=False, dry_run=False, verbose=0)
```
<hr>

### `Promote.predict()`
The `Promote.predict()` method sends data to a deployed model via REST API request and returns a prediction.

**Usage**

`p.predict(modelName, data, username=None)`

**Arguments**
- `modelName`(_string_): Name of the model you'd like to query
- `data`(_list_ or _dict_): Data you'd like to send to the model to be scored
- `username`(_string_, optional): Username of the model you'd like to query. This will default to the one set in the Promote constructor. However if you'd like to query another person's model or a production model, this will come in handy.

**Example:**
```python
p.predict("MyFirstPythonModel", json.loads(testdata), username=None)
```
<hr>

### `requirements.txt`
The `requirements.txt` file is how to specify the libraries that should be installed by the promote app upon deployment of the model. The `promote` library should always be listed in addition to any other model dependencies. You are also able to specify the version of each library that should be installed.

**Example:**
```shell
promote
pandas
pyodbc==4.0.24
```

You can also install dependencies hosted on public or private hosted git repositories using a well-formatted https link (SSH is currently not supported). If the repository is private, you will need to first create a personal access token. Refer to the documentation for your hosting provider for best practices in structuring this link. Generally, a link with the following format will work:
```
git+https://x-access-token:<yourPersonalAccessToken>@git.yourHostingProvider.com/username/packageName.git
```

You can also target a specific branch, tag or commit SHA. See the pip docs for more on how to structure these links:

```
git+http://git.yourHostingProvider.com/username/packageName.git@myBranch
git+http://git.yourHostingProvider.com/username/packageName.git@myTag
git+http://git.yourHostingProvider.com/username/packageName.git@myFullCommitHash
```
<hr>

### `promote.sh`
The `promote.sh` file can be included in your model directory. It is executed before your model is built and can be used to install low-level system packages such as Linux packages and other dependencies.

**Example:**
```shell
# Install Microsoft SQL Server RHEL7 ODBC Driver
curl https://packages.microsoft.com/config/rhel/7/prod.repo > /etc/yum.repos.d/mssql-release.repo

exit
yum remove unixODBC-utf16 unixODBC-utf16-devel #to avoid conflicts
ACCEPT_EULA=Y yum install msodbcsql17
# optional: for bcp and sqlcmd
ACCEPT_EULA=Y yum install mssql-tools
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
source ~/.bashrc
```
<hr>

### <a name="helpers"></a>`helpers` Directory
Users can also add a `helpers` directory to the root directory of their project to store helper scripts that are used by the deployment script. Please refer to the [Model Directory Structure](#directory) above for an example. Adding an `__init__.py` file to the `helpers` directory will allow the python files in the directory to be discoverable via the python `import` command.

**Example:**
```python
from helpers import helper_funs
```
<hr>

### <a name="objects"></a>`objects` Directory
Users can also add an `objects` directory to the root directory of their project to store helper scripts that are used by the deployment script. Please refer to the [Model Directory Structure](#directory) above for an example. The `objects` directory is a great place to put pretrained models and other model dependencies. It is a best practice to train models outside of the `deploy.py` script and to save the trained model to the `objects` directory. This prevents the Promote app from attempting to retrain the model on each redeploy.

**Example:**
```python
my_model = pickle.load( open( "./objects/my_model.p", "rb" ) )
```
<hr>

### Deployment
Currently, the only way to deploy a python model is to execute the `deploy.py` script from a command line terminal. To do this, open a command line window, navigate to the root project directory and run the following:
```python
python deploy.py
```

## Upgrade Python dependencies when deploying a model
[Upgrade Python dependencies when deploying a model](examples/check_env/upgrade-dependencies.md)
