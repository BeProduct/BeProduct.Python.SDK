"""
File: _common_apps.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: Apps Mixin for every master folder
"""


class AppsMixin:
    """
    Apps mixin class for every master folder
    """

    def app_schema(self, app_id: str):
        """ Returns an app schema
        :app_id: ID of the application / page
        :returns: Dictionary with app schema data
        """
        return self.client.raw_api.get(
            f"{self.master_folder}/PageSchema?pageId={app_id}")

    def app_list(self, header_id: str):
        """ Returns list of apps/pages
        for a specific style, material, etc

        :header_id: ID of the style, material, etc
        :returns: List of apps
        """
        return self.client.raw_api.get(
            f"{self.master_folder}/Pages?headerId={header_id}")

    def app_get(self, header_id: str, app_id: str):
        """ Returns a particular app

        :header_id: ID of the style, material, etc
        :app_id: ID of the application / page
        :returns: Dictionary with app data
        """
        return self.client.raw_api.get(
            f"{self.master_folder}/Page?headerId={header_id}&pageId={app_id}")

    def app_form_update(self, header_id: str, app_id: str, fields):
        """ Updates form application
        :header_id: ID of the style, material, etc
        :app_id: ID of the application / page
        :fields: Dictionary of fields to update {'field_id':'value'}
        """
        return self.client.raw_api.post(
            f"{self.master_folder}/PageForm?headerId={header_id}&pageId={app_id}",
            body=[{'id': field_id, 'value': fields[field_id]} for field_id in fields])

    def app_grid_update(self, header_id: str, app_id: str, rows):
        """ Updates form application
        :header_id: ID of the style, material, etc
        :app_id: ID of the application / page
        :rows: List of row dictionaries
        """
        return self.client.raw_api.post(
            f"{self.master_folder}/PageGrid?headerId={header_id}&pageId={app_id}",
            body=rows)

    def app_list_update(self, header_id: str, app_id: str, list_items):
        """ Updates List application
        :header_id: ID of the style, material, etc
        :app_id: ID of the application / page
        :list_items: Items of the list app
        """
        return self.client.raw_api.post(
            f"{self.master_folder}/PageList?headerId={header_id}&pageId={app_id}",
            body=list_items)

    def app_attachments_delete(
            self,
            header_id: str,
            app_id: str,
            filenames_to_remove):
        """ Deletes files from Attachments app
        :header_id: ID of the style, material, etc
        :app_id: ID of the application / page
        :filenames_to_remove: List of filenames to be removed
        """
        return self.client.raw_api.post(
            f"{self.master_folder}/AttachmentRemove?headerId={header_id}&pageId={app_id}",
            body=filenames_to_remove)
