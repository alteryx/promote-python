## Weather model
### Overview

This model takes in latitude and longitude, requests the current weather from the Darksky API, and then maps that value to a list of "feels like" descriptions, such as "mild".

**Project structure:**

```
weather-model/
├── README.md
├── helpers
│   ├── __init__.py
│   ├── datatable.csv
│   ├── get_weather.py
│   └── tempdesc.py
├── main.py
└── requirements.txt
```

### Instructions

**NOTE:** In order for this model to deploy, you must have a Darksky API Key.  You can get one here: https://darksky.net/dev

In a terminal shell run:

```bash
$ pip install requirements.txt

# lastly, deploy the model
$ python main.py
```

### Example input:

```
{"lat":"37", "lon":"-122"}
```

### Result

```
{
  "tempature": 73.67, 
  "feels": "Warm"
}
```