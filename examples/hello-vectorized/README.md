## Hello World
### Overview

This model accepts:

```
[
    {"id": 1, "name": "your_name"}, 
    {"id": 2, "name": "your_friends_name"}
]
```

and returns:

```
[
    {'greeting': 'Hello your_name!', 'id': 1},
    {'greeting': 'Hello your_friends_name!', 'id': 2}
]
```

**Project structure:**

```
├── README.md
├── main.py
└── requirements.txt
```

### Instructions

In a terminal shell run:

```bash
$ pip install requirements.txt

# lastly, deploy the model
$ python main.py
```
