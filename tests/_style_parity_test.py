"""
File: _style_parity_test.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct

Live tests for the Style methods added for parity with the TypeScript SDK.
Writes run against throwaway styles created in STYLE_FOLDER and deleted in
tearDown. Tests that need a fixture the tenant config does not define skip
and name the key that would enable them.
"""

import os
import unittest
import uuid
import warnings
import test_helpers
from test_config import TestConfiguration


class TestStyleParity(unittest.TestCase):
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
        test_helpers.cleanup(self)

    def _need(self, *keys):
        missing = [k for k in keys if not hasattr(self.config, k)]
        if missing:
            self.skipTest(f"tenant config lacks {', '.join(missing)}")

    # ── schemas / reads ──────────────────────────────────────────────

    def test_folder_size_range_schema(self):
        schema = self.client.style.folder_size_range_schema(self.config.STYLE_FOLDER["id"])
        self.assertIsInstance(schema, list)

    def test_folder_search_schema(self):
        schema = self.client.style.folder_search_schema(self.config.STYLE_FOLDER["id"])
        self.assertTrue(isinstance(schema, (list, dict)))

    def test_app_request_schema(self):
        # Needs a tracking REQUEST app (isSampleApp), not the regular sample
        # request page — Request/PageSchema answers "Page not found" for the latter.
        self._need("REQUEST_APP")
        schema = self.client.style.app_request_schema(self.config.REQUEST_APP["id"])
        self.assertTrue(isinstance(schema, (list, dict)))

    def test_attributes_where_used_in_sets(self):
        used = self.client.style.attributes_where_used_in_sets(self.config.STYLE["id"])
        self.assertIsInstance(used, list)

    def test_flat_bom(self):
        page = self.client.style.flat_bom({}, page_size=5, page_number=0)
        self.assertTrue(isinstance(page, (list, dict)))

    # ── app-level writes on a throwaway style ────────────────────────

    def test_app_reset(self):
        # A fresh style has no page document for an app until something writes
        # to it, and Reset on a missing page is "Page not found." — so write first.
        tmp = test_helpers.create_tmp_style(self)
        app = self.config.FORMGRID_APP["id"]
        form = self.client.style.app_get(tmp["id"], app)["data"]["form"]
        field = next(f for f in form if f["type"] == "Text")
        self.client.style.app_form_update(tmp["id"], app, {field["id"]: "before-reset"})
        self.assertEqual(self._form_value(tmp["id"], app, field["id"]), "before-reset")

        self.client.style.app_reset(tmp["id"], app)

        self.assertIn(self._form_value(tmp["id"], app, field["id"]), (None, ""))

    def _form_value(self, header_id, app_id, field_id):
        form = self.client.style.app_get(header_id, app_id)["data"]["form"]
        return next(f["value"] for f in form if f["id"] == field_id)

    def test_app_bom_item_delete(self):
        tmp = test_helpers.create_tmp_style(self)
        bom = self.config.BOM_APP["id"]
        self.client.style.app_bom_update(tmp["id"], bom, [{"materialIdToInsert": self.config.MATERIAL_HEADER["id"]}])
        rows = self.client.style.app_get(tmp["id"], bom)["data"]["data"]
        self.assertEqual(len(rows), 1)

        self.client.style.app_bom_item_delete(tmp["id"], bom, rows[0]["rowId"])

        self.assertEqual(self.client.style.app_get(tmp["id"], bom)["data"]["data"], [])

    def test_app_bom_reset(self):
        tmp = test_helpers.create_tmp_style(self)
        bom = self.config.BOM_APP["id"]
        self.client.style.app_bom_update(tmp["id"], bom, [{"materialIdToInsert": self.config.MATERIAL_HEADER["id"]}])

        self.client.style.app_bom_reset(tmp["id"], bom)

        self.assertEqual(self.client.style.app_get(tmp["id"], bom)["data"]["data"], [])

    def test_app_bom_details_update(self):
        self._need("BOM_DETAILS_UPDATE")  # {"app_id": ..., "materials": [...]}
        tmp = test_helpers.create_tmp_style(self)
        u = self.config.BOM_DETAILS_UPDATE
        self.client.style.app_bom_details_update(tmp["id"], u["app_id"], u["materials"])

    def test_app_multimeasurements_update(self):
        self._need("UPDATE_TEST")
        ut = self.config.UPDATE_TEST
        mm = ut["multiMeasurements"]
        marker = f"parity-{uuid.uuid4().hex[:6]}"
        self.client.style.app_multimeasurements_update(
            ut["styleId"], mm["appId"],
            {"sizeClass": mm["sizeClassId"], "poms": [{"id": mm["pomId"], "code": "MPM", "pointOfMeasure": marker}]},
        )
        after = self.client.style.app_get(ut["styleId"], mm["appId"])
        self.assertIn(marker, str(after))

    def test_app_multimeasurements_reset(self):
        tmp = test_helpers.create_tmp_style(self)
        self.client.style.app_multimeasurements_reset(tmp["id"], self.config.MULTIMEASUREMENTS_APP["id"])
        self.assertIn("data", self.client.style.app_get(tmp["id"], self.config.MULTIMEASUREMENTS_APP["id"]))

    def test_app_textlist_update_editor_and_upload(self):
        tmp = test_helpers.create_tmp_style(self)
        app = self.config.TEXTLIST_APP["id"]
        item_id = str(uuid.uuid4())

        self.client.style.app_textlist_update(tmp["id"], app, [{"itemId": item_id, "itemFields": [{"id": "text", "value": "tl-item"}]}])
        self.client.style.app_textlist_editor_update(tmp["id"], app, "<p>hello from parity test</p>")

        after = self.client.style.app_get(tmp["id"], app)["data"]
        self.assertIn("hello from parity test", after["text"] or "")
        self.assertTrue(any(i.get("id") == item_id for i in after["images"]))

        upload_id = self.client.style.app_textlist_upload(tmp["id"], app, item_id, filepath=self.image_path)
        self.assertTrue(upload_id)
        self.assertTrue(test_helpers.check_upload_status(self, upload_id))

    @unittest.expectedFailure
    def test_app_sets_update(self):
        # Style/PageSets answers 500 ArgumentNullException ('source') on the
        # integration tenant as of 2026-09-04 — reproduced with the identical
        # payload through the TypeScript SDK, so it is the endpoint, not this
        # wrapper. expectedFailure flips to "unexpected success" once fixed.
        tmp = test_helpers.create_tmp_style(self)
        app = self.config.SETS_APP["id"]
        row_id = str(uuid.uuid4())
        self.client.style.app_sets_update(tmp["id"], app, [
            {"styleIdToInsert": self.config.STYLE["id"],
             "styleUpdate": {"rowId": row_id, "rowFields": [{"id": "group", "value": "Main"}]}},
        ])
        rows = self.client.style.app_get(tmp["id"], app)["data"]["data"]
        self.assertGreaterEqual(len(rows), 1)

    def test_app_imagegrid_list_update(self):
        tmp = test_helpers.create_tmp_style(self)
        app = self.config.IMAGEGRID_APP["id"]
        item_id = str(uuid.uuid4())
        self.client.style.app_imagegrid_list_update(tmp["id"], app, [{"itemId": item_id, "itemFields": [{"id": "text", "value": "ig-list-item"}]}])
        images = self.client.style.app_get(tmp["id"], app)["data"]["image"]
        self.assertTrue(any(i.get("id") == item_id for i in images))

    def test_app_link_pages_update(self):
        self._need("LINK_PAGES_UPDATE")  # {"app_id": ..., "items": [...]}
        tmp = test_helpers.create_tmp_style(self)
        u = self.config.LINK_PAGES_UPDATE
        self.client.style.app_link_pages_update(tmp["id"], u["app_id"], u["items"])

    def test_app_sample_request_multi_add_submit(self):
        self._need("SAMPLE_REQUEST_MULTI_ADD_SUBMIT")  # {"app_id": ..., "data": {...}}
        tmp = test_helpers.create_tmp_style(self)
        u = self.config.SAMPLE_REQUEST_MULTI_ADD_SUBMIT
        self.client.style.app_sample_request_multi_add_submit(tmp["id"], u["app_id"], u["data"])

    def test_app_artboard_image_assign(self):
        self._need("ARTBOARD_IMAGE_ASSIGN")  # request body dict
        self.client.style.app_artboard_image_assign(self.config.ARTBOARD_IMAGE_ASSIGN)

    # ── header-level writes ──────────────────────────────────────────

    def test_attributes_carry_over(self):
        tmp = test_helpers.create_tmp_style(self)
        copy = self.client.style.attributes_carry_over(tmp["id"], skip_colorways=True)
        self.assertIn("id", copy)
        self.assertNotEqual(copy["id"], tmp["id"])
        self.trash_bin["TMP_STYLE_IDS"].append(copy["id"])

    def test_attributes_colorways_delete(self):
        style = self.client.style.attributes_create(
            folder_id=self.config.STYLE_FOLDER["id"],
            fields=self.config.TMP_STYLE_ATTRIBUTES_FIELDS,
            colorways=self.config.TMP_STYLE_COLORWAY_FIELDS,
        )
        self.trash_bin["TMP_STYLE_IDS"].append(style["id"])
        ids = [c["id"] for c in style["colorways"]]
        self.assertGreater(len(ids), 0)

        self.client.style.attributes_colorways_delete(style["id"], ids)

        self.assertEqual(self.client.style.attributes_get(style["id"])["colorways"], [])

    def test_attributes_update_sample_size(self):
        style = self.client.style.attributes_create(
            folder_id=self.config.STYLE_FOLDER["id"],
            fields=self.config.TMP_STYLE_ATTRIBUTES_FIELDS,
            sizes=self.config.TMP_STYLE_SIZES,
        )
        self.trash_bin["TMP_STYLE_IDS"].append(style["id"])
        size_class_id = style["sizeClasses"][0]["id"]
        target = self.config.TMP_STYLE_SIZES[1]["name"]

        self.client.style.attributes_update_sample_size(style["id"], size_class_id, target)

        after = self.client.style.attributes_get(style["id"])
        sample = [s["name"] for s in after["sizeRange"] if s.get("isSampleSize")]
        self.assertEqual(sample, [target])

    def test_attributes_block_link_unlink(self):
        self._need("BLOCK_HEADER")
        tmp = test_helpers.create_tmp_style(self)
        self.client.style.attributes_block_link(tmp["id"], self.config.BLOCK_HEADER["id"])
        self.client.style.attributes_block_unlink(tmp["id"])

    def test_attributes_move(self):
        self._need("STYLE_FOLDER_2")
        tmp = test_helpers.create_tmp_style(self)
        self.client.style.attributes_move(tmp["id"], self.config.STYLE_FOLDER_2["id"])
        self.assertEqual(self.client.style.attributes_get(tmp["id"])["folder"]["id"], self.config.STYLE_FOLDER_2["id"])


if __name__ == "__main__":
    unittest.main()
