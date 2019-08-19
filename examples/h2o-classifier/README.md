## H2O Iris Classifier
### Overview

This model uses the H2O python library to train a RandomForest classifier to predict flower species.

### Important notes about H2O models

There are three steps that are special for H2O models:

1. Creating a promote.sh file for installing the Java dependency with your model.
2. Setting the maximum memory for your model using `max_mem_size` when you initialize your H2O model.
3. Releasing the prediction data from your H2O server session after each prediction using `h2o.remove()`.

These are explained in further detail below:

#### Installing Java Dependency

You will need to deploy your model with a `promote.sh` script file in the base of your model foler (next to your deployment script). There is one in the repo that you can copy. It's a shell script that will run during the building of your model and will install the Java dependacy that's required to run H2O models. It looks like this:
  
```bash
#!/bin/bash

apt-get update
apt-get install -y default-jdk
```

#### Setting Max Memory

Alteryx recommends limiting the amount of memory that h2o can consume with the `max_mem_size` flag when you initialize H2O in your model code.
The defualt is 4GB, which is likely more than you need! This number will depend on the size of your model, but 100MB is a good place to start.

Here's an example:

```Python
h2o.init(max_mem_size='100m')
```

See http://docs.h2o.ai/h2o/latest-stable/h2o-py/docs/h2o.html?highlight=remove#h2o.init for more information.

#### Releasing prediction data

H2O will automatically hold on to the input and prediction data, which is a feature we don't need in Promote and will consume a lot of memory if you're sending a lot of requests to a model and will eventually lead to dropped predictions and high latency.
You must use h2o.remove() to remove this data from H2O's memory.

Here's an example:

```Python
h2o.remove(h2o_data)
h2o.remove(prediction)
```

See http://docs.h2o.ai/h2o/latest-stable/h2o-py/docs/h2o.html?highlight=remove#h2o.remove for more information.

Just follow our example and you'll be in good shape!

**Project structure:**

```
h2o-classifier/
├── README.md
├── deploy.py
├── iris.csv
├── objects
│   └── h2o_rf_model
├── promote.sh
├── requirements.txt
└── train.pyy
```

### Instructions

In a terminal shell run:

```bash
$ pip install requirements.txt

# next, train the model
$ python train.py

# finally, deploy the model
$ python deploy.py
```

### Example input:

```
{"C1":4.9,"C2":3,"C3":1.4,"C4":0.2}
```

### Result

```
{
  "result": {
    "response": {
      "predict": {
        "0": "Iris-setosa"
      },
      "Iris-setosa": {
        "0": 0.9956357962858318
      },
      "Iris-versicolor": {
        "0": 0
      },
      "Iris-virginica": {
        "0": 0.004364203714168255
      }
    }
  },
}
```
