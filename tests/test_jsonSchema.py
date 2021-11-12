from __future__ import absolute_import, division, print_function

import unittest
from JsonSchema import jsonschema 


class TestJsonSchemaGenerator(unittest.TestCase):
    js=jsonschema()
    def test_empty_object(self):
        expected = {'type': 'array', 'properties': {}}
        self.assertEqual(self.js.guess_schema({}), expected)

    def test_string(self):
        expected = {'type': 'string'}
        self.assertEqual(self.js.guess_schema(''), expected)
        
    def test_list(self):
        expected = {'type': 'enum', 'items': {}}
        self.assertEqual(self.js.guess_schema([]), expected)

    def test_list_with_items(self):
        expected = {'type': 'enum', 'items': {'type': 'integer'}}
        self.assertEqual(self.js.guess_schema([1, 2, 3]), expected)

    def test_object_with_nested_properties(self):
        expected ={'type': 'array',
         'properties': {'something': {'required': False,
           'tag': '',
           'description': '',
           'type': 'array',
           'properties': {'nested_required': {'required': False,
             'tag': '',
             'description': '',
             'type': 'string'}}}}}
        self.assertEqual(self.js.guess_schema({"something": {"nested_required": "1"}}),
                         expected)