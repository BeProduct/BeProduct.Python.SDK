"""
File: _master_data.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: Master Data (field definitions) Public API
"""

from .sdk import BeProduct, BeProductAsync


class MasterData:
    """Implements Master Data API — company-wide and per-folder field definitions"""

    def __init__(self, client: BeProduct | BeProductAsync):
        """Constructor"""
        self.client = client

    def get(self, field_id: str):
        """Gets a master data field definition

        :field_id: Field ID
        :returns: Field definition

        """
        return self.client.raw_api.get(f"MasterData/{field_id}")

    def create(self, fields):
        """Creates a master data field

        :fields: Field definition dictionary
        :returns: Created field

        """
        return self.client.raw_api.post("MasterData/Create", body=fields)

    def update(self, field_id: str, fields):
        """Updates a master data field

        :field_id: Field ID
        :fields: Field definition dictionary

        """
        return self.client.raw_api.post(f"MasterData/{field_id}/Update", body=fields)

    def folder_field_get(self, folder_id: str, field_id: str):
        """Gets a field definition as configured for one folder

        :folder_id: Folder ID
        :field_id: Field ID
        :returns: Field definition

        """
        return self.client.raw_api.get(f"MasterData/Field/{folder_id}/{field_id}")

    def folder_field_update(self, folder_id: str, field_id: str, fields):
        """Updates a field definition for one folder

        :folder_id: Folder ID
        :field_id: Field ID
        :fields: Field definition dictionary

        """
        return self.client.raw_api.post(f"MasterData/Field/{folder_id}/{field_id}/Update", body=fields)
