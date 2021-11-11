"""
File: _common_upload_test.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
"""

import os
import uuid
import unittest
import warnings
import test_helpers
from test_config import TestConfiguration


class TestUploadMixin(unittest.TestCase):

    def setUp(self):
        warnings.simplefilter('ignore', category=DeprecationWarning)

        self.image_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'assets', '1kb.jpg')

        if not hasattr(self, 'config'):
            self.config = TestConfiguration()
            self.client = test_helpers.get_beproduct_client(self.config)
            self.trash_bin = test_helpers.get_empty_trash_bin()

    def tearDown(self):
        # cleanup resources
        test_helpers.cleanup(self)

    def test_attributes_upload(self):
        """Attributes upload"""

        tmp_style = test_helpers.create_tmp_style(self)
        _, fname = os.path.split(self.image_path)

        # regular upload
        upload_id = self.client.style.attributes_upload(
            header_id=tmp_style['id'],
            filepath=self.image_path)
        self.assertTrue(test_helpers.check_upload_status(self, upload_id))

        style = self.client.style.attributes_get(header_id=tmp_style['id'])
        self.assertTrue(style['headerData']['frontImage']
                        ['origin'].endswith(fname))

        # position upload
        upload_id = self.client.style.attributes_upload(
            header_id=tmp_style['id'],
            filepath=self.image_path,
            position='back')

        self.assertTrue(test_helpers.check_upload_status(self, upload_id))

        style = self.client.style.attributes_get(header_id=tmp_style['id'])
        self.assertTrue(style['headerData']['backImage']
                        ['origin'].endswith(fname))

    def test_app_list_upload(self):
        """App List upload"""

        tmp_style = test_helpers.create_tmp_style(self)
        item_id = str(uuid.uuid4())
        _, fname = os.path.split(self.image_path)

        def get_app(): return self.client.style.app_get(
            header_id=tmp_style['id'],
            app_id=self.config.LIST_APP['id'])

        # item insert
        self.client.style.app_list_update(
            header_id=tmp_style['id'],
            app_id=self.config.LIST_APP['id'],
            list_items=[{
                'itemId': item_id,
                'itemFields': self.config.LIST_APP_ITEM_INSERT
            }])

        app = get_app()
        item = list(filter(lambda r: r['id'] ==
                           item_id, app['data']))

        self.assertTrue(len(item) == 1)

        self.client.style.app_list_upload(
            header_id=tmp_style['id'],
            app_id=self.config.LIST_APP['id'],
            list_item_id=item_id,
            filepath=self.image_path)

        app = get_app()
        item = list(filter(lambda r: r['id'] ==
                           item_id, app['data']))

        self.assertTrue(len(item) == 1)
        self.assertTrue(item[0]['origin'].endswith(fname))

    def test_app_attachments_upload(self):
        """App Attachments upload"""

        tmp_style = test_helpers.create_tmp_style(self)
        _, fname = os.path.split(self.image_path)

        self.client.style.app_attachments_upload(
            header_id=tmp_style['id'],
            app_id=self.config.ATTACHMENTS_APP['id'],
            filepath=self.image_path)

        app = self.client.style.app_get(
            header_id=tmp_style['id'],
            app_id=self.config.ATTACHMENTS_APP['id']
        )
        self.assertTrue(app['data']['files'][0]['url'].endswith(fname))

    def test_app_imageform_upload(self):
        """App ImageForm upload"""

        tmp_style = test_helpers.create_tmp_style(self)
        _, fname = os.path.split(self.image_path)

        upload_id = self.client.style.app_imageform_upload(
            header_id=tmp_style['id'],
            app_id=self.config.IMAGEFORM_APP['id'],
            filepath=self.image_path)
        self.assertTrue(test_helpers.check_upload_status(self, upload_id))

        app = self.client.style.app_get(
            header_id=tmp_style['id'],
            app_id=self.config.IMAGEFORM_APP['id']
        )
        self.assertTrue(app['data']['image'][0]['origin'].endswith(fname))

    def test_app_imagegrid_upload(self):
        """App ImageGrid upload"""

        tmp_style = test_helpers.create_tmp_style(self)
        _, fname = os.path.split(self.image_path)

        upload_id = self.client.style.app_imagegrid_upload(
            header_id=tmp_style['id'],
            app_id=self.config.IMAGEFORM_APP['id'],
            filepath=self.image_path)
        self.assertTrue(test_helpers.check_upload_status(self, upload_id))

        app = self.client.style.app_get(
            header_id=tmp_style['id'],
            app_id=self.config.IMAGEFORM_APP['id']
        )
        self.assertTrue(app['data']['image'][0]['origin'].endswith(fname))


if __name__ == '__main__':
    unittest.main(verbosity=2)
