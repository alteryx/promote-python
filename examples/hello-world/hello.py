#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""hello.py
"""
import promote
from schema import Schema, And


# schema is optional
@promote.validate_json(Schema({'name': And(str, len)}))
def promoteModel(data):
    return data

username = 'austin'
api_key = '9a9773e8e8946c651c86fa6c651c86fa'
url = "https://sandbox.c.yhat.com/"

p = promote.Promote(username, api_key, url)

# test data
testdata = {'name': 'austin'}

# test model locally
promoteModel(testdata)

# 1. test that testdata is valid json
# 2. THERE IS test data, run promoteModel(testdata) before deployment

p.deploy("HelloModel1", testdata, verbose=2)
# p.deploy("HelloModel", testdata, confirm=True, dry_run=False, verbose=0)

