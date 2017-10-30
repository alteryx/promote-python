import unittest
import promote
import logging
import copy
import base64
import pickle
from schema import Schema, And
import sys
import os

class Tests(unittest.TestCase):
    def setUp(self):
        self.p = promote.Promote('fakeuser', 'fakeapike', 'https://www.fakeurl.com/')
        self.p.deployment_file = os.path.join(os.path.dirname(__file__), 'sample-model', 'deploy_clfModel.py')
        self.p.deployment_dir = os.path.dirname(self.p.deployment_file)
    
    def testInitSetsDeploymentFileCorrectly(self):
        self.assertEqual(self.p.deployment_file,
                         'tests/sample-model/deploy_clfModel.py')
    
    def testInvalidDeploymentFile(self):
        originalArgv = copy.copy(sys.argv)
        sys.argv[0] = 'foo'
        try:
            promote.Promote('fakeuser', 'fakeapike', 'https://www.fakeurl.com/')
            raise Exception("shouldn't get here")
        except Exception as ex:
            self.assertIsNotNone(ex)
        sys.argv = originalArgv

    def testInitSetsDeploymentDirCorrectly(self):
        self.assertEqual(self.p.deployment_dir,
                         'tests/sample-model')
    
    def testInvalidDeploymentDir(self):
        # TODO: this is just a subset of testInvalidDeploymentFile. it's a stupid test.
        originalArgv = copy.copy(sys.argv)
        sys.argv[0] = 'foo'
        try:
            promote.Promote('fakeuser', 'fakeapike', 'https://www.fakeurl.com/')
            raise Exception("shouldn't get here")
        except Exception as ex:
            self.assertIsNotNone(ex)
        sys.argv = originalArgv

    def testReadRequirementsFile(self):
        self.assertEqual(3, len(self.p._get_requirements().split('\n')))

    def testMissingRequirementsFile(self):
        self.p.deployment_dir = '/non-existant-directory'
        try:
            self.p._get_requirements()
            raise Exception("shouldn't get here")
        except Exception as ex:
            self.assertIsNotNone(ex)

    def testGetObjectsMissingPickleDir(self):
        self.p.deployment_dir = '/non-existant-directory'
        self.assertEqual({}, self.p._get_objects())

    def testGetObjects(self):
        self.assertEqual(2, len(self.p._get_objects()))
    
    def testGetObjectsAreSerializeable(self):
        objects = self.p._get_objects()
        value = objects['rng.pkl']
        obj = base64.decodebytes(bytes(value, 'utf-8'))
        self.assertIsNotNone(pickle.loads(obj))

    def testGetSourceForModel(self):
        def testFunction():
            pass
        extracted_code = self.p._get_function_source_code(testFunction)
        actual_file = os.path.join(
            os.path.dirname(__file__), 'sample-model', 'deploy_clfModel.py'
        )
        with open(actual_file, 'r') as f:
            actual_code = f.read()
        actual_code += '\npromoteModel = testFunction\n'

        self.assertEqual(extracted_code, actual_code)

    def testGetSourceErrorsWhenPromoteModelNotFound(self):
        self.p.deployment_file = os.path.join(
            os.path.dirname(__file__), 'sample-model', 'deploy_malformed.py')

        try:
            self.p._get_function_source_code()
            raise Exception("shouldn't get here")
        except Exception as ex:
            self.assertIsNotNone(ex)

    def testJsonValidatorWrongSchema(self):
        try:
            @promote.validate_json('not a schema object')
            def test_function(data):
                return data
        except Exception as ex:
            self.assertIsNotNone(ex)

    def testJsonValidatorValidJSON(self):
        @promote.validate_json(Schema({'name': And(str, len)}))
        def test_function(data):
            return data

        testdata = {'name': 'Alteryx'}
        self.assertEqual(testdata, test_function(testdata))

    def testJsonValidatorInvalidJSON(self):
        @promote.validate_json(Schema({'name': And(str, len)}))
        def test_function(data):
            return data

        testdata = {'name': True}
        try:
           test_function(testdata)
        except Exception as ex:
            self.assertIsNotNone(ex)

    def testModelName(self):
        try:
            testdata = { 'name': 'Alteryx' }
            def test_function(data):
                return data

            self.p.deploy("MyF$%^&Model", test_function, testdata, confirm=False)
        except Exception as ex:
            self.assertIsNotNone(ex)
        
if __name__ == '__main__':
    unittest.main()
