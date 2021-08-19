"""
File: _common_attributes_test.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
"""

import unittest
import warnings
import test_helpers
from test_config import TestConfiguration


class TestAttributesMixin(unittest.TestCase):

    def setUp(self):
        warnings.simplefilter('ignore', category=DeprecationWarning)

        if not hasattr(self, 'config'):
            self.config = TestConfiguration()
            self.client = test_helpers.get_beproduct_client(self.config)
            self.cleanup_list = []

    def tearDown(self):
        # cleanup resources
        pass

    def test_folders(self):
        """ List folders """
        folders = self.client.style.folders()

        # Checking result
        self.assertIsInstance(folders, list)
        test_folder = test_helpers.get_first(
            lambda f: f['id'] == self.config.STYLE_FOLDER['id'], folders)
        self.assertTrue(test_folder, "Can't find folder in a list")
        self.assertDictContainsSubset(
            self.config.STYLE_FOLDER,
            test_folder)

    def test_folder_schema(self):
        """ Get folder schema """
        folder_schema = self.client.style.folder_schema(
            folder_id=self.config.STYLE_FOLDER['id'])

        # Checking result
        self.assertIsInstance(folder_schema, list)
        self.assertIn('fieldId', folder_schema[0])

    def test_attributes_list(self):
        """ Searching attributes """
        fields_filtered = self.client.style.attributes_list(
            filters=[{
                'field': 'header_number',
                'value': self.config.STYLE['headerNumber'],
                'operator': 'Eq'
            }])
        self.assertDictContainsSubset(self.config.STYLE, next(fields_filtered))

        colorway_filtered = self.client.style.attributes_list(
            colorway_filters=[{
                'field': 'color_number',
                'value': self.config.STYLE['colorways'][0]['colorNumber'],
                'operator': 'Eq'
            }])
        self.assertDictContainsSubset(
            self.config.STYLE, next(colorway_filtered))

    def test_attributes_get(self):
        """ Get single attributes """

        self.assertDictContainsSubset(
            self.config.STYLE,
            self.client.style.attributes_get(
                header_id=self.config.STYLE['id']
            ))

    def test_attributes_delete(self):
        """ Delete style """

        tmp_style = self.client.style.attributes_create(
            folder_id=self.config.STYLE_FOLDER['id'],
            fields=self.config.TMP_STYLE_ATTRIBUTES_FIELDS)

        self.assertEquals(
            tmp_style,
            self.client.style.attributes_get(header_id=tmp_style['id']))

        self.client.style.attributes_delete(header_id=tmp_style['id'])

        with self.assertRaisesRegex(Exception, 'Style not found'):
            self.client.style.attributes_get(header_id=tmp_style['id'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
