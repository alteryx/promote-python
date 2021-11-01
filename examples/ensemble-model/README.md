## Ensemble Model
### Overview

This example trains 3 classifier models and then combines them to form an ensemble model.

**Project structure:**

```
ensemble-model/
├── README.md
├── main.py
├── models
│   ├── __init__.py
│   ├── decisiontree.py
│   ├── ensemble.py
│   ├── knn.py
│   └── svc.py
├── objects
│   └── svc.pkl
├── requirements.txt
└── train.py
```

### Instructions

In a terminal shell run:

```bash
$ pip install -r requirements.txt

# train the models

$ python train.py

# lastly, deploy the model
$ python main.py
```

### Example input:

```
[[5.1, 3.5], [6.7, 3.1]]
```

### Result

```
[
    {"prediction": [0.00432478257037855, 0.980898817870272, 0.014776399559349595]},
    {"prediction": [0.03754032205261976, 0.9399860049855375, 0.022473672961842786]}
]
```