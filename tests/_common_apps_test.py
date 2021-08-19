"""
File: _common_apps_test.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
"""

import unittest
import warnings
import test_helpers
from test_config import TestConfiguration


class TestAppsMixin(unittest.TestCase):

    def setUp(self):
        warnings.simplefilter('ignore', category=DeprecationWarning)

        if not hasattr(self, 'config'):
            self.config = TestConfiguration()
            self.client = test_helpers.get_beproduct_client(self.config)
            self.cleanup_list = []

    def tearDown(self):
        # cleanup resources
        pass

    def test_app_schema(self):
        """ Get app schema """
        form_app_id = list(filter(
            lambda i: i['type'] == 'Form',
            self.config.STYLE_APP_LIST
        ))[0]['id']

        self.assertDictContainsSubset(
            self.config.STYLE_APP_SCHEMA,
            self.client.style.app_schema(form_app_id))

    def test_app_list(self):
        """ Listing style app """
        app_list = self.client.style.app_list(
            header_id=self.config.STYLE['id'])
        for app in self.config.STYLE_APP_LIST:
            self.assertIn(app, app_list)

    def test_app_get(self):
        """ Getting Apps """
        def test_app(app_dict):
            self.assertDictContainsSubset(
                app_dict,
                self.client.style.app_get(
                    header_id=self.config.STYLE['id'],
                    app_id=app_dict['id']))

        for app in [
                self.config.FORM_APP,
                self.config.GRID_APP]:
            test_app(app)

    def test_app_form_update(self):
        """ App Form Update """
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
