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
                         os.path.join(os.path.dirname(__file__),
                                      'sample-model', 'deploy_clfModel.py'))
    
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
                         os.path.dirname(self.p.deployment_file))
    
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
    
    def testReadPromoteshFile(self):
        self.assertEqual(1, len(self.p._get_promote_sh().split('\n')))

    def testMissingRequirementsFile(self):
        self.p.deployment_dir = '/non-existant-directory'
        try:
            self.p._get_requirements()
            raise Exception("shouldn't get here")
        except Exception as ex:
            self.assertIsNotNone(ex)

    def testGetObjectsMissingPickleDir(self):
        self.p.deployment_dir = '/non-existant-directory'
        try:
            self.p._get_objects()
            raise Exception("shouldn't get here")
        except Exception as ex:
            self.assertIsNotNone(ex)

    def testGetObjects(self):
        self.assertEqual(2, len(self.p._get_objects()))

    def testGetObjectsObjects(self):
        objects, tarName = self.p._get_objects()
        self.assertEqual(2, len(objects))
    
    def testGetObjectsReturnsObjects(self):
        (objects, tarName) = self.p._get_objects()
        self.assertIsNotNone(objects['rng.pkl'])

    def testGetObjectsReturnsTarname(self):
        (objects, tarName) = self.p._get_objects()
        self.assertIsNotNone(tarName)

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

    def testModelNameLength(self):
        try:
            testdata = { 'name': 'Alteryx' }
            def test_function(data):
                return data

            self.p.deploy("Modelsupersupersupersupersuperlongmodelname", test_function, testdata, confirm=False)
        except Exception as ex:
            self.assertIsNotNone(ex)

    def testModelMetadata(self):
        try:
            self.p.metadata.one = 1
            self.p.metadata.two = 2
            self.p.metadata['three'] = 'three'
            self.p.metadata['comment'] = 'this is a rather lengthy comment'
            self.p.metadata.array = [0, 1, 'two']
            self.p.metadata.dict = {'a': 1, 'b': 'two'}
            self.assertEqual(self.p.metadata, 
                {
                    "one": 1,
                    "two": 2,
                    "three": "three",
                    "comment": "this is a rather lengthy comment",
                    'array': [0, 1, 'two'],
                    'dict': {'a': 1, 'b': 'two'}
                })
        except Exception as ex:
            self.assertIsNone(ex)

    def testModelMetaDataSixLimit(self):
        try:
            self.p.metadata.a = 1
            self.p.metadata.b = 2
            self.p.metadata.c = 3
            self.p.metadata.d = 4
            self.p.metadata.e = 5
            self.p.metadata.f = 6
            self.p.metadata.g = 7
        except Exception as ex:
            self.assertEqual(str(ex), 'Metadata items limit exceeded. Max allowed is 6.')

    def testModelMetaDataKeyLengthLimit(self):
        try:
            self.p.metadata['thiskeyislongerthan20characters'] = 1
        except Exception as ex:
            self.assertEqual(
                str(ex), 'Maximum metadata key characters of 20 exceeded. Your key has 31 characters')

    def testModelMetaDataValueLengthLimit(self):
        try:
            self.p.metadata['key'] = 'this is a very long value, in fact it is too long'
        except Exception as ex:
            self.assertEqual(
                str(ex), 'Maximum metadata value characters of 50 exceeded. Your value has 51 characters')

if __name__ == '__main__':
    unittest.main()
