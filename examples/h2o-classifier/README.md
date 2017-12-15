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
│   └── DRF_model_python_1512530312673_3
├── requirements.txt
└── train.py
```

### Instructions

In a terminal shell run:

```bash
$ pip install requirements.txt

# next, train the model
$ pyhton train.py

# finally, deploy the model
$ python main.py
```

### Example input:

```
{"C1":4.9,"C2":3,"C3":1.4,"C4":0.2}
```

### Result

```
{'response': 
    {'predict': 
        {0: 'Iris-setosa'},
        'Iris-setosa': {0: 0.99897540982272015},
        'Iris-versicolor': {0: 0},
        'Iris-virginica': {0: 0.0010245901772798741}
    }
}
```