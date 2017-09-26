## Database Lookup
### Overview

Each time a request is sent to this model, it opens a connection to a PostgreSQL database and returns a query result.

**Project structure:**

```
db-lookup/
├── README.md
├── main.py
├── helpers
│   ├── __init__.py
│   └── dbconn.py
└── requirements.txt
```

### Instructions

**NOTE:** In order for this model to deploy, you must have a Postgres database running on localhost:5444 with a table called `users` and a column named `username`.

In a terminal shell run:

```bash
$ pip install requirements.txt

# start your PostgreSQL database

# lastly, deploy the model
$ python main.py
```

### Example input:

```
{"id": "f9471423-7537-4e03-949b-1fb521cfffd1"}
```

### Result

```
  {
    "id": "f9471423-7537-4e03-949b-1fb521cfffd1",
    "username": "greg",
    "favoritefood": "pizza-bagels",
    "favoritesport": "baseball"
  }
```