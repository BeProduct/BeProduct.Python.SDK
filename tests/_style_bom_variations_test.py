"""
File: _style_bom_variations_test.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct

Live tests for the BOM Variations app. They need a tenant config
(tests/configs/<domain>.json) that names an app with variations ENABLED:

    "BOM_VARIATIONS_APP":   "<BOMVariations application id>",
    "BOM_VARIATIONS_STYLE": "<a style id in that app's folder with >= 1 variation>",
    "BOM_VARIATIONS_ALLOW_WRITES": true   # opt-in: the write test creates & deletes a variation

Without the first two keys every test here is skipped; without the third the
write cycle is skipped. Listing a variations-DISABLED app creates its default
variation server-side, so never point these at such an app.
"""

import unittest
import uuid
import warnings
import test_helpers
from test_config import TestConfiguration


class TestStyleBomVariations(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", category=DeprecationWarning)
        if not hasattr(self, "config"):
            self.config = TestConfiguration()
            self.client = test_helpers.get_beproduct_client(self.config)
        if not (hasattr(self.config, "BOM_VARIATIONS_APP") and hasattr(self.config, "BOM_VARIATIONS_STYLE")):
            self.skipTest("tenant config has no BOM_VARIATIONS_APP / BOM_VARIATIONS_STYLE")
        self.app_id = self.config.BOM_VARIATIONS_APP
        self.style_id = self.config.BOM_VARIATIONS_STYLE

    def test_bom_variation_schema(self):
        """Schema has the two field sets and the enabled flag"""
        schema = self.client.style.app_bom_variation_schema(self.app_id)
        self.assertTrue(schema["enableBomVariations"])
        self.assertIsInstance(schema["metadata"], list)
        self.assertGreater(len(schema["grid"]), 0)

    def test_bom_variation_list(self):
        """List is always a list of variation metadata"""
        variations = self.client.style.app_bom_variation_list(self.style_id, self.app_id)
        self.assertIsInstance(variations, list)
        self.assertGreater(len(variations), 0)
        for v in variations:
            self.assertIn("id", v)
            self.assertIn("variationName", v)
            self.assertNotIn("rows", v)  # rows come from app_bom_variation_get

    def test_bom_variation_get(self):
        """Single variation carries metadata and rows"""
        first = self.client.style.app_bom_variation_list(self.style_id, self.app_id)[0]
        v = self.client.style.app_bom_variation_get(self.style_id, self.app_id, first["id"])
        self.assertEqual(v["id"], first["id"])
        self.assertIn("metadata", v)
        self.assertIsInstance(v["rows"], list)
        for row in v["rows"]:
            self.assertIn("rowId", row)
            self.assertIsInstance(row["fields"], list)

    def test_bom_variation_write_cycle(self):
        """create -> update -> reset -> delete on a variation this test owns"""
        if not getattr(self.config, "BOM_VARIATIONS_ALLOW_WRITES", False):
            self.skipTest("BOM_VARIATIONS_ALLOW_WRITES is not enabled for this tenant")

        name = f"sdk-test-{uuid.uuid4().hex[:8]}"
        created = self.client.style.app_bom_variation_create(
            self.style_id, self.app_id, {"variationName": name, "syncColorways": True}
        )
        variation_id = created["id"]
        try:
            self.assertEqual(created["metadata"]["variationName"], name)

            updated = self.client.style.app_bom_variation_update(
                self.style_id, self.app_id, variation_id, {"variationName": name + "-renamed"}
            )
            self.assertEqual(updated["metadata"]["variationName"], name + "-renamed")

            reset = self.client.style.app_bom_variation_reset(self.style_id, self.app_id, variation_id)
            self.assertEqual(reset["rows"], [])
        finally:
            self.client.style.app_bom_variation_delete(self.style_id, self.app_id, variation_id)

        ids = [v["id"] for v in self.client.style.app_bom_variation_list(self.style_id, self.app_id)]
        self.assertNotIn(variation_id, ids)


if __name__ == "__main__":
    unittest.main()
