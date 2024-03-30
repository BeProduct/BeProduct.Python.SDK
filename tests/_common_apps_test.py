"""
File: _common_apps_test.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
"""

import os
import unittest
import uuid
import warnings
import test_helpers
from test_config import TestConfiguration


class TestAppsMixin(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", category=DeprecationWarning)

        self.image_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "assets", "1kb.jpg"
        )

        if not hasattr(self, "config"):
            self.config = TestConfiguration()
            self.client = test_helpers.get_beproduct_client(self.config)
            self.trash_bin = test_helpers.get_empty_trash_bin()

    def tearDown(self):
        # cleanup resources
        test_helpers.cleanup(self)

    def test_app_schema(self):
        """Get app schema"""
        form_app_id = list(
            filter(lambda i: i["type"] == "Form", self.config.STYLE_APP_LIST)
        )[0]["id"]

        equals, msg = test_helpers.is_subset_or_equals(
            self.config.STYLE_APP_SCHEMA, self.client.style.app_schema(form_app_id)
        )
        self.assertTrue(equals, msg)

    def test_app_list(self):
        """Listing style apps"""
        app_list = self.client.style.app_list(header_id=self.config.STYLE["id"])
        for app in self.config.STYLE_APP_LIST:
            self.assertIn(app, app_list)

    def test_app_get(self):
        """Getting Apps"""

        def test_app(app_dict):
            a = app_dict
            b = self.client.style.app_get(
                header_id=self.config.STYLE["id"], app_id=app_dict["id"]
            )
            self.assertTrue(*test_helpers.is_subset_or_equals(a, b))

        for app in [
            self.config.FORM_APP,
            self.config.GRID_APP,
            self.config.LIST_APP,
            self.config.ATTACHMENTS_APP,
            self.config.IMAGEFORM_APP,
            self.config.IMAGEGRID_APP,
        ]:
            test_app(app)

    def test_app_form_update(self):
        """App Form Update"""

        tmp_style = test_helpers.create_tmp_style(self)

        self.client.style.app_form_update(
            header_id=tmp_style["id"],
            app_id=self.config.FORM_APP["id"],
            fields=self.config.FORM_APP_UPDATE,
        )

        form_app = self.client.style.app_get(
            header_id=tmp_style["id"], app_id=self.config.FORM_APP["id"]
        )

        for field in self.config.FORM_APP_UPDATED["data"]:
            self.assertIn(field, form_app["data"])

        self.client.style.app_form_update(
            header_id=tmp_style["id"],
            app_id=self.config.IMAGEFORM_APP["id"],
            fields=self.config.IMAGEFORM_APP_UPDATE,
        )

        form_app = self.client.style.app_get(
            header_id=tmp_style["id"], app_id=self.config.IMAGEFORM_APP["id"]
        )

        for field in self.config.IMAGEFORM_APP_UPDATED:
            self.assertIn(field, form_app["data"]["form"])

    def test_app_grid_update(self):
        """App Grid Update"""
        tmp_style = test_helpers.create_tmp_style(self)

        def get_app():
            return self.client.style.app_get(
                header_id=tmp_style["id"], app_id=self.config.GRID_APP["id"]
            )

        row_id = str(uuid.uuid4())

        # row insert
        self.client.style.app_grid_update(
            header_id=tmp_style["id"],
            app_id=self.config.GRID_APP["id"],
            rows=[{"rowId": row_id, "rowFields": self.config.GRID_APP_ROW_INSERT}],
        )

        app = get_app()
        row = list(filter(lambda r: r["rowId"] == row_id, app["data"]["gridData"]))

        self.assertTrue(len(row) == 1)
        for field in self.config.GRID_APP_ROW_INSERTED:
            self.assertIn(field, row[0]["fields"])

        # row update
        self.client.style.app_grid_update(
            header_id=tmp_style["id"],
            app_id=self.config.GRID_APP["id"],
            rows=[{"rowId": row_id, "rowFields": self.config.GRID_APP_ROW_UPDATE}],
        )

        app = get_app()
        row = list(filter(lambda r: r["rowId"] == row_id, app["data"]["gridData"]))

        self.assertTrue(len(row) == 1)
        for field in self.config.GRID_APP_ROW_UPDATED:
            self.assertIn(field, row[0]["fields"])

        # row delete
        self.client.style.app_grid_update(
            header_id=tmp_style["id"],
            app_id=self.config.GRID_APP["id"],
            rows=[
                {
                    "rowId": row_id,
                    "rowFields": [],  # TODO: remove this line
                    "deleteRow": True,
                }
            ],
        )

        app = get_app()
        row = list(filter(lambda r: r["rowId"] == row_id, app["data"]["gridData"]))

        self.assertTrue(len(row) == 0)

        # SAME FOR IMAGEGRID
        def get_imagegrid_app():
            return self.client.style.app_get(
                header_id=tmp_style["id"], app_id=self.config.IMAGEGRID_APP["id"]
            )

        # row insert
        self.client.style.app_grid_update(
            header_id=tmp_style["id"],
            app_id=self.config.IMAGEGRID_APP["id"],
            rows=[{"rowId": row_id, "rowFields": self.config.IMAGEGRID_APP_ROW_INSERT}],
        )

        app = get_imagegrid_app()
        row = list(
            filter(lambda r: r["rowId"] == row_id, app["data"]["grid"]["gridData"])
        )

        self.assertTrue(len(row) == 1)
        for field in self.config.IMAGEGRID_APP_ROW_INSERTED:
            self.assertIn(field, row[0]["fields"])

        # row update
        self.client.style.app_grid_update(
            header_id=tmp_style["id"],
            app_id=self.config.IMAGEGRID_APP["id"],
            rows=[{"rowId": row_id, "rowFields": self.config.IMAGEGRID_APP_ROW_UPDATE}],
        )

        app = get_imagegrid_app()
        row = list(
            filter(lambda r: r["rowId"] == row_id, app["data"]["grid"]["gridData"])
        )

        self.assertTrue(len(row) == 1)
        for field in self.config.IMAGEGRID_APP_ROW_UPDATED:
            self.assertIn(field, row[0]["fields"])

        # row delete
        self.client.style.app_grid_update(
            header_id=tmp_style["id"],
            app_id=self.config.IMAGEGRID_APP["id"],
            rows=[
                {
                    "rowId": row_id,
                    "rowFields": [],  # TODO: remove this line
                    "deleteRow": True,
                }
            ],
        )

        app = get_imagegrid_app()
        row = list(
            filter(lambda r: r["rowId"] == row_id, app["data"]["grid"]["gridData"])
        )

        self.assertTrue(len(row) == 0)

    def test_app_list_update(self):
        """App List Update"""
        tmp_style = test_helpers.create_tmp_style(self)

        def get_app():
            return self.client.style.app_get(
                header_id=tmp_style["id"], app_id=self.config.LIST_APP["id"]
            )

        item_id = str(uuid.uuid4())

        # item insert
        self.client.style.app_list_update(
            header_id=tmp_style["id"],
            app_id=self.config.LIST_APP["id"],
            list_items=[
                {"itemId": item_id, "itemFields": self.config.LIST_APP_ITEM_INSERT}
            ],
        )

        app = get_app()
        item = list(filter(lambda r: r["id"] == item_id, app["data"]))

        self.assertTrue(len(item) == 1)
        for field in self.config.LIST_APP_ITEM_INSERTED:
            self.assertIn(field, item[0]["controls"])

        # item update
        self.client.style.app_list_update(
            header_id=tmp_style["id"],
            app_id=self.config.LIST_APP["id"],
            list_items=[
                {"itemId": item_id, "itemFields": self.config.LIST_APP_ITEM_UPDATE}
            ],
        )

        app = get_app()
        item = list(filter(lambda r: r["id"] == item_id, app["data"]))

        self.assertTrue(len(item) == 1)
        for field in self.config.LIST_APP_ITEM_UPDATED:
            self.assertIn(field, item[0]["controls"])

        # item delete
        self.client.style.app_list_update(
            header_id=tmp_style["id"],
            app_id=self.config.LIST_APP["id"],
            list_items=[{"itemId": item_id, "deleteItem": True}],
        )

        app = get_app()
        item = list(filter(lambda r: r["id"] == item_id, app["data"]))
        self.assertTrue(len(item) == 0)

    def test_app_attachments_delete(self):
        """App Attachments Delete files"""
        tmp_style = test_helpers.create_tmp_style(self)
        _, fname = os.path.split(self.image_path)

        self.client.style.app_attachments_upload(
            header_id=tmp_style["id"],
            app_id=self.config.ATTACHMENTS_APP["id"],
            filepath=self.image_path,
        )

        app = self.client.style.app_get(
            header_id=tmp_style["id"], app_id=self.config.ATTACHMENTS_APP["id"]
        )
        self.assertTrue(fname in app["data"]["files"][0]["url"])

        self.client.style.app_attachments_delete(
            header_id=tmp_style["id"],
            app_id=self.config.ATTACHMENTS_APP["id"],
            filenames_to_remove=[os.path.splitext(fname)[0]],
        )

        app = self.client.style.app_get(
            header_id=tmp_style["id"], app_id=self.config.ATTACHMENTS_APP["id"]
        )
        self.assertTrue(len(app["data"]["files"]) == 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
