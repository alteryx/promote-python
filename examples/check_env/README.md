## heckEnv
### Overview

This model will check and returns the versions of Python and its dependencies.

It's used to verify the [upgrades for the versions of Python and its dependencies](upgrade-dependencies.md)

**Project structure:**

```
├── README.md
├── main.py
├── promote.sh
└── requirements.txt
```

### Instructions

In a terminal shell run:

```bash
$ pip install requirements.txt

# lastly, deploy the model
$ python main.py
```

### Example input:

```
{}
```

### Result

```
{
  "status": "OK",
  "timestamp": "2021-10-20T19:27:15.636Z",
  "result": {
    "Python_version": "3.8.5 |Anaconda, Inc.| (default, Apr 29 2018, 16:14:56) \n[GCC 7.2.0]",
    "requests_version": "2.22.0"
  },
  "promote_id": "2a688633-bf61-44a1-b46e-c754163dde0e",
  "model_name": "HelloModel",
  "model_version": "1"
}
```