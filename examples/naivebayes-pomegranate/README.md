## Naive Bayes Classifier
### Overview

This model builds a Naive Bayes Classifier, using the [pomegrante](http://pomegranate.readthedocs.io/en/latest/) package.

**NOTE:** This model requires Python version >= 3.7. To upgrade Python version, please visit: 

* [Upgrade for the versions of Python and its dependencies](examples/check_env/upgrade-dependencies.md)

* [Check upgrades for the versions of Python and its dependencies](examples/check_env/README.md)


In building this model, we save the Classifier to the `/objects` directory for future use.

### Example 

This model accepts:

```
[19.08025296, -2.94031655, 9.06747934, 3.30080305, 1.62963848]
```

and returns:

```
[1]
```

**Project structure:**

```
├── README.md
├── deploy.py
├── objects
│   └── naive_weights.pomo
├── requirements.txt
└── train-naivebayes.py
```

### Instructions

In a terminal shell run:

```bash
$ pip install -r requirements.txt

# next, train the model
$ python train-naivebayes.py

# lastly, deploy the model
$ python deploy.py
```
