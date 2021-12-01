## Iris Flower Classification

Project structure:

```
├── README.md
├── deploy.py
├── helpers
│   └── getclass.py
├── objects
│   └── model_weights.pkl
├── promote.sh
├── requirements.txt
└── train.py
```

### Instructions

In a terminal shell run:

```bash
$ pip install promote

# first train the model (this will generate the model_weights.pkl file)
$ python train.py

# lastly, deploy the model
$ python main.py
```

Example input:

[[5.1, 3.5, 1.4, 0.2], [6.7, 3.1, 5.6, 2.4]]


