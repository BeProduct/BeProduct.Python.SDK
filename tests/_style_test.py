"""
File: _style_test.py
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


class TestStyleMixin(unittest.TestCase):
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

    def test_folder_colorway_schema(self):
        """Test folder schema"""

        colorway_field_schemas = self.client.style.folder_colorway_schema(
            folder_id=self.config.STYLE_FOLDER["id"]
        )

        for field in self.config.STYLE_FOLDER_COLORWAY_SCHEMA:
            self.assertIn(field, colorway_field_schemas)

    def test_attributes_update(self):
        """Test attributes update"""

        tmp_style = test_helpers.create_tmp_style(self)
        updated_style = self.client.style.attributes_update(
            header_id=tmp_style["id"], fields={"header_name": "updated header name"}
        )
        self.assertEquals("updated header name", updated_style["headerName"])

    def test_attributes_create(self):
        """Creating attributes"""

        tmp_style = self.client.style.attributes_create(
            folder_id=self.config.STYLE_FOLDER["id"],
            fields=self.config.TMP_STYLE_ATTRIBUTES_FIELDS,
            colorways=self.config.TMP_STYLE_COLORWAY_FIELDS,
            sizes=self.config.TMP_STYLE_SIZES,
        )

        for field in self.config.TMP_STYLE_CREATED["headerData"]["fields"]:
            self.assertIn(field, tmp_style["headerData"]["fields"])

        for color in self.config.TMP_STYLE_CREATED["colorways"]:
            tmp_colorway = list(
                filter(
                    lambda r: r["colorNumber"] == color["colorNumber"],
                    tmp_style["colorways"],
                )
            )[0]
            self.assertTrue(*test_helpers.is_subset_or_equals(color, tmp_colorway))

        self.assertTrue(
            *test_helpers.is_subset_or_equals(
                self.config.TMP_STYLE_CREATED["sizeRange"], tmp_style["sizeRange"]
            )
        )

        self.trash_bin["TMP_STYLE_IDS"].append(tmp_style["id"])

    def test_attributes_colorway_delete(self):
        """Deleting style colorway"""
        tmp_style = self.client.style.attributes_create(
            folder_id=self.config.STYLE_FOLDER["id"],
            fields=self.config.TMP_STYLE_ATTRIBUTES_FIELDS,
            colorways=self.config.TMP_STYLE_COLORWAY_FIELDS,
        )
        self.trash_bin["TMP_STYLE_IDS"].append(tmp_style["id"])

        color_to_delete = tmp_style["colorways"][0]

        self.client.style.attributes_colorway_delete(
            header_id=tmp_style["id"], colorway_id=color_to_delete["id"]
        )

        tmp_style = self.client.style.attributes_get(header_id=tmp_style["id"])

        self.assertTrue(
            len(
                list(
                    filter(
                        lambda r: r["id"] == color_to_delete["id"],
                        tmp_style["colorways"],
                    )
                )
            )
            == 0
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
