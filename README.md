# Alteryx Promote Python Client
Python library for deploying models built using Python to Alteryx Promote.

### Installation
```
pip install promote
```
### Examples

[Hello World](examples/hello-world)
[Article Summarizer](examples/article-summarizer)
[DB Lookup](examples/db-lookup)
[Ensemble Model](examples/ensemble-model)
[Iris Classifier](examples/iris-classifier)
[Weather Model](examples/weather-model)

### Project Overview

In order for all of your model dependencies to be transfered over to Alteryx Promote, you project must follow a particular structure.

#### Example model directory structure:
```
example-model/
├── promote.sh
├── main.py (our deployment script)
├── helpers (optional)
│   ├── __init__.py
│   ├── summarizer.py
├── objects (optional)
│   └── svc.pkl
└── requirements.txt (required)
```

`promote.sh` - this file is executed before your model is built.  It can be used to install low-level system packages such as Linux packages.

`main.py` - our primary model deployment script

`helpers/` - a directory where helper functions can be saved.

`objects/` - a directory where pickle files or other data files needed for model execution can be saved.

`requirements.txt` - a list of our python package requirements.  

## Building a model:

Before beginning building a model, be sure to import the `promote` package:

`import promote`

### The `promoteModel()` function

The `promoteModel` function is used to define the API endpoint for a model and is executed each time a model is called.  **This is the core of the API endpoint**

```python
# import the promote package and define our model function
import promote

def helloWorld(data):
    return {'response': 'Hello ' + data['name'] + '!'}

# specify the username, apikey and url, and then deploy
USERNAME = 'your_username'
API_KEY = 'your_apikey'
PROMOTE_URL = "https://promote.yourcompany.com"

p = promote.Promote(USERNAME, API_KEY, PROMOTE_URL)

# execute locally with test data
TESTDATA = {'name': 'Colin'}
HelloModel(TESTDATA)
# {'response': 'Hello Colin!'}


p.deploy("HelloModel", helloWorld, TESTDATA, confirm=True, dry_run=False, verbose=1)

# Send a request to the model
p.predict("HelloModel", {"name": "greg"})

# { 'result': {'response': 'Hello greg!'}},
# 'version': 1,
# 'promote_id': '9fbcb56a89bf318d8b50c41654554e3c',
# 'promote_model': 'HelloModel'}
```

<hr>

### The `@promote.validate_json` decoractor

`@promote.validate_json` is an optional decorator that can be useful for validating data as it comes into a model.  It utilizes the `schema` package to validate JSON.

#### Usage

`from schema import Schema`
`@promote.validate_json(Schema({'name': And(str, len)}))`

```python
import promote

@promote.validate_json(Schema({'name': And(str, lambda s: len(s) > 1)}))
def helloModel(data):
    return {'response': 'Hello ' + data['name'] + '!'}
```

The code above ensures that all data passed to our model must:

1. Be an object, `{}`
2. Contain the key `'name'`
3. Contain a string with length greater than 1 character.

### Setting the Auth

To deploy models, you'll need to add your username, API key, and URL of Promote to a new instance of the class `Promote`
```python
p = promote.Promote(USERNAME, API_KEY, PROMOTE_URL)
```
<hr>

### `Promote`

The `Promote` module has 2 methods:

- [`Promote.deploy`](#promotedeploy)
- [`Promote.predict`](#promotepredict)

### `Promote.deploy`

#### Deploy a model to Alteryx Promote

The `deploy` function captures `promoteModel()`, any objects in the `helpers/` and `objects/` directories, the `promote.sh` file, and send them to the Promote servers.

#### Usage

`Promote.deploy(name, model, testdata, confirm=False, dry_run=False, verbose=0)`

`p.deploy("HelloWorld", helloModel, TESTDATA, confirm=False)`

#### Arguments
- `name`(_string_):  the name of the model to deploy to Alteryx Promote
- `model`: the name of the promoteModel function
- `testdata`(_object_): a valid data object that your model can predict on
- `confirm` (_boolean_, optional): If `True`, then user will be prompted to confirm deployment
- `dry_run` (_boolean_, optional): If `True`, tests to see that the model can be pickled; model does not deploy
- `verbose` (_int_, optional): Integer between 0 and 4, determines verbosity of logging during deployment.

#### Examples

Deploy the "LPOptimizer_model" and don't require confirmation on deployment.
```python
p.deploy("LPOptimizer_model", LPModel, TESTDATA, confirm=False)
```
Below, `dry_run=True` builds the model, prints the dependencies but does not deploy the model.
```python
p.deploy("LPOptimizer_model", LPModel, TESTDATA, dry_run=True)
```
<hr>

### `Promote.predict()`

Send data to a model via REST API request from R for a prediction.

#### Usage

`Promote.predict(model, data)`

#### Arguments
- `model`(_string_): the name of your model
- `data`: data required to make a single prediction. This can be a dict or dataframe

#### Example
```python
p.predict("LPOptimizer_model", {"activities": ["sleep", "work", "leisure"], "required_hours": [7, 10, 0], "happiness_per_hour": [1.5, 1, 2]})
```