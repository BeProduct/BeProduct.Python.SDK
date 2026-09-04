"""
File: _api_parity_test.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct

Live tests for the Inbox, Data Tables, Master Data, Line Sheets and Reports
APIs, and for the additional Tracking / Directory / Users / Material / Image /
Color / Block methods. Reads run against tenant fixtures; writes skip unless
the tenant config opts in with the named key.
"""

import os
import unittest
from itertools import islice
import warnings
import test_helpers
from test_config import TestConfiguration


class _Base(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", category=DeprecationWarning)
        self.image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets", "1kb.jpg")
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

    @staticmethod
    def _first(iterable):
        for item in iterable:
            return item
        return None


class TestInbox(_Base):
    def test_task_list(self):
        tasks = list(islice(self.client.inbox.task_list("Style", page_size=5), 5))
        self.assertIsInstance(tasks, list)

    def test_task_get_and_messages(self):
        task = self._first(self.client.inbox.task_list("Style", page_size=1))
        if task is None:
            self.skipTest("tenant has no inbox tasks")
        got = self.client.inbox.task_get(task["id"])
        self.assertEqual(got["id"], task["id"])
        self.assertIsInstance(list(islice(self.client.inbox.message_list(task["id"], page_size=5), 5)), list)

    def test_task_and_message_write_cycle(self):
        self._need("INBOX_WRITES")  # {"task": {...create body...}, "message": {...}}
        w = self.config.INBOX_WRITES
        task = self.client.inbox.task_create(w["task"])
        try:
            self.client.inbox.task_update(task["id"], {**w["task"], "subject": "parity-updated"})
            msg = self.client.inbox.message_create(task["id"], w["message"])
            self.client.inbox.message_update(msg["id"], {**w["message"], "text": "edited"})
            upload_id = self.client.inbox.message_attachments_upload(msg["id"], filepath=self.image_path)
            self.assertTrue(upload_id)
            self.client.inbox.message_delete(msg["id"])
        finally:
            self.client.inbox.task_delete(task["id"])


class TestDataTables(_Base):
    def test_list_schema_and_data(self):
        table = self._first(self.client.data_tables.list(page_size=1))
        if table is None:
            self.skipTest("tenant has no data tables")
        schema = self.client.data_tables.schema(table["id"])
        self.assertTrue(isinstance(schema, (list, dict)))
        rows = list(islice(self.client.data_tables.data(table["id"], page_size=5), 5))
        self.assertIsInstance(rows, list)

    def test_update_and_reset(self):
        self._need("DATA_TABLE_WRITES")  # {"id": ..., "rows": [...]}
        w = self.config.DATA_TABLE_WRITES
        self.client.data_tables.update(w["id"], w["rows"])
        self.client.data_tables.reset(w["id"])


class TestMasterData(_Base):
    def test_get(self):
        self._need("MASTER_DATA_FIELD")
        field = self.client.master_data.get(self.config.MASTER_DATA_FIELD["fieldId"])
        self.assertTrue(isinstance(field, (list, dict)))

    def test_folder_field_get(self):
        # The per-folder endpoint wants a field from THAT folder's schema, not a
        # company-level master data field — take the first attribute field.
        self._need("STYLE_FOLDER")
        folder_id = self.config.STYLE_FOLDER["id"]
        field_id = self.client.style.folder_schema(folder_id)[0]["fieldId"]
        field = self.client.master_data.folder_field_get(folder_id, field_id)
        self.assertTrue(isinstance(field, (list, dict)))

    def test_writes(self):
        self._need("MASTER_DATA_WRITES")  # {"create": {...}, "update": {"fieldId":..., "data": {...}}}
        w = self.config.MASTER_DATA_WRITES
        self.client.master_data.create(w["create"])
        self.client.master_data.update(w["update"]["fieldId"], w["update"]["data"])


class TestLineSheets(_Base):
    def test_folders_list_get(self):
        folders = self.client.linesheets.folders()
        self.assertIsInstance(folders, list)
        sheets = self.client.linesheets.list()
        self.assertIsInstance(sheets, list)
        if sheets:
            got = self.client.linesheets.get(sheets[0]["id"])
            self.assertEqual(got["id"], sheets[0]["id"])


class TestReports(_Base):
    def test_list(self):
        reports = list(islice(self.client.reports.list(page_size=5), 5))
        self.assertIsInstance(reports, list)

    def test_flat_bom(self):
        page = self.client.reports.flat_bom({}, page_size=5, page_number=0)
        self.assertTrue(isinstance(page, (list, dict)))

    def test_data(self):
        self._need("REPORT_DATA")  # {"id": ..., "body": {...}}
        w = self.config.REPORT_DATA
        page = self.client.reports.data(w["id"], w["body"], page_size=5, page_number=0)
        self.assertTrue(isinstance(page, (list, dict)))


class TestTracking(_Base):
    def _plan_id(self):
        plan = self._first(self.client.tracking.plan_list())
        if plan is None:
            self.skipTest("tenant has no tracking plans")
        return plan["id"]

    def test_progress(self):
        plan_id = self._plan_id()
        self.assertTrue(isinstance(self.client.tracking.plan_style_progress(plan_id), (list, dict)))
        self.assertTrue(isinstance(self.client.tracking.plan_material_progress(plan_id), (list, dict)))

    def test_revisions(self):
        plan_id = self._plan_id()
        self.assertIsInstance(list(islice(self.client.tracking.plan_style_revisions(plan_id), 5)), list)
        self.assertIsInstance(list(islice(self.client.tracking.plan_material_revisions(plan_id), 5)), list)

    def test_writes(self):
        self._need("TRACKING_WRITES")  # {"planId":..., "styleIds":[...], "materialIds":[...]}
        w = self.config.TRACKING_WRITES
        self.client.tracking.plan_style_add(w["planId"], w["styleIds"])
        self.client.tracking.plan_material_add(w["planId"], w["materialIds"])
        timelines = list(self.client.tracking.plan_style_timeline_list(w["planId"]))
        ids = [t["id"] for t in timelines if t.get("headerId") in w["styleIds"]]
        if ids:
            self.client.tracking.plan_style_timelines_archive(w["planId"], ids)
            self.client.tracking.plan_style_timelines_delete(w["planId"], ids)


class TestDirectory(_Base):
    def test_search(self):
        found = list(islice(self.client.directory.directory_search(page_size=5), 5))
        self.assertIsInstance(found, list)

    def test_updates(self):
        self._need("DIRECTORY_WRITES")  # {"directoryId":..., "fields": {...}, "contactId":..., "contactFields": {...}}
        w = self.config.DIRECTORY_WRITES
        self.client.directory.directory_update(w["directoryId"], w["fields"])
        self.client.directory.directory_contact_update(w["directoryId"], w["contactId"], w["contactFields"])


class TestUsers(_Base):
    def test_get_by_id(self):
        self._need("USERS_FIRST")
        user = self.client.user.user_get_by_id(self.config.USERS_FIRST["id"])
        self.assertEqual(user["id"], self.config.USERS_FIRST["id"])


class TestMaterial(_Base):
    def test_folder_size_range_schema(self):
        self._need("MATERIAL_FOLDER")
        schema = self.client.material.folder_size_range_schema(self.config.MATERIAL_FOLDER["id"])
        self.assertIsInstance(schema, list)

    def test_writes(self):
        self._need("MATERIAL_WRITES")  # {"headerId":..., "colorwayIds":[...], "targetFolderId":..., "app3d": {"appId":..., "data": {...}}}
        w = self.config.MATERIAL_WRITES
        self.client.material.attributes_colorways_delete(w["headerId"], w["colorwayIds"])
        self.client.material.app_3d_material_update(w["headerId"], w["app3d"]["appId"], w["app3d"]["data"])
        self.client.material.attributes_move(w["headerId"], w["targetFolderId"])


class TestImage(_Base):
    def test_image_version_upload(self):
        self._need("IMAGE_WRITES")  # {"headerId": ...}
        upload_id = self.client.image.attributes_image_version_upload(self.config.IMAGE_WRITES["headerId"], filepath=self.image_path)
        self.assertTrue(upload_id)


class TestColor(_Base):
    def test_folder_color_chip_schema(self):
        self._need("COLOR_FOLDER")
        schema = self.client.color.folder_color_chip_schema(self.config.COLOR_FOLDER["id"])
        self.assertIsInstance(schema, list)

    def test_company_colors(self):
        colors = list(islice(self.client.color.company_colors(page_size=5), 5))
        self.assertIsInstance(colors, list)


class TestBlock(_Base):
    def test_size_class_assets(self):
        self._need("BLOCK_HEADER")  # {"id": ..., "sizeClassId": ...}
        b = self.config.BLOCK_HEADER
        assets = self.client.block.attributes_size_class_assets(b["id"], b["sizeClassId"])
        self.assertTrue(isinstance(assets, (list, dict)))


if __name__ == "__main__":
    unittest.main()
