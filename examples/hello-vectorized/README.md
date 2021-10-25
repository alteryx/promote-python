## Hello World Vectorized
### Overview

This model shows how to process multiple rows of data in a single request.  It is based on the "Hello World" model.

### Example 

This model accepts:

```
[
    {"id": 1, "name": "Colin"}, 
    {"id": 2, "name": "Ross"}
]
```

and returns:

```
[
    {'id': 1, 'greeting': 'Hello Colin!'}, 
    {'id': 2, 'greeting': 'Hello Ross!'}
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
$ pip install -r requirements.txt

# lastly, deploy the model
$ python main.py
```
