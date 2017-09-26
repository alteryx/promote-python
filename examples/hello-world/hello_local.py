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

username = 'colin'
api_key = 'd580d451-06b9-4c10-a73f-523adca5f48c'
url = "http://localhost:3001"

p = promote.Promote(username, api_key, url)

# test data
testdata = {'name': 'austin'}

# test model locally
promoteModel(testdata)

# 1. test that testdata is valid json
# 2. THERE IS test data, run promoteModel(testdata) before deployment

p.deploy("HelloModel1", testdata, verbose=2)
# p.deploy("HelloModel", testdata, confirm=True, dry_run=False, verbose=0)

