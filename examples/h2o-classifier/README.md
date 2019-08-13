## H2O Iris Classifier
### Overview

This model uses the h2o python library to train a RandomForest classifier to predict flower species.

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
