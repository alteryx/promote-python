## Jupyter Notebook - SVC
### Overview

This example shows how to deploy a model when you're developing in Jupyter Notebook.

Because Promote only accepts command-line deployments, you will need to download your `.ipynb` file as a `.py` file and execute it.

### Instructions


In a terminal shell run:

```bash
$ jupyter notebook SVC_Classifier.ipynb

# next update your username / apikey and create a .py file
jupyter nbconvert --to script SVC_Classifier.ipynb

# lastly, execute the new python script
$ python SVC_Classifier.py
```

### Example 

This model accepts:

```
{
    "0":{"0":5.1},
    "1":{"0":3.5},
    "2":{"0":1.4},
    "3":{"0":0.2}
}
```

and returns:

```
['setosa']
```

**Project structure:**

```
├── README.md
├── SVC_Classifier.ipynb
└── requirements.txt
```
