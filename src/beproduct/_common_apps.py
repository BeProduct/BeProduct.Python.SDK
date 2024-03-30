"""
File: _common_apps.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: Apps Mixin for every master folder
"""

import logging
from functools import lru_cache


class AppsMixin:
    """
    Apps mixin class for every master folder
    """

    class __BlackBox:
        """All BlackBoxes are the same."""

        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

        def __eq__(self, other):
            return isinstance(other, type(self))

        def __hash__(self):
            return hash(type(self))

    def app_schema(self, app_id: str):
        """Returns an app schema
        :app_id: ID of the application / page
        :returns: Dictionary with app schema data
        """
        return self.client.raw_api.get(
            f"{self.master_folder}/PageSchema?pageId={app_id}"
        )

    @lru_cache(maxsize=128)
    def __app_list(self, bb: __BlackBox, folder_id: str):
        logging.debug("APP_LIST: Cache miss. Fetching fresh data.")
        return self.client.raw_api.get(
            f"{self.master_folder}/Pages?headerId={bb.header_id}"
        )

    def app_list(self, header_id: str, folder_id: str = None):
        """Returns list of apps/pages for a specific style, material, etc
        :header_id: ID of the style, material, etc
        :folder_id: ID of the folder
        :returns: List of apps
        Note: If folder_id is provided, result may be cached to speed up the response
        """
        if folder_id:
            logging.debug("APP_LIST: Folder_id provided. Fetching cached data.")
            return self.__app_list(self.__BlackBox(header_id=header_id), folder_id)
        else:
            logging.debug(
                "APP_LIST: Cache is disable because folder_id is not provided. Fetching fresh data."
            )
            return self.client.raw_api.get(
                f"{self.master_folder}/Pages?headerId={header_id}"
            )

    def app_get(
        self,
        header_id: str,
        app_id: str = None,
        app_name: str = None,
        folder_id: str = None,
    ):
        """Returns a particular app

        :header_id: ID of the style, material, etc
        :app_id: ID of the application / page
        :app_name: Name of the application / page. Case is irrelevant.
        :folder_id: ID of the folder
        :returns: Dictionary with app data

        Note: Either app_id or app_name should be provided
        Also if folder_id is provided, result may be cached to speed up the response
        """
        if not app_id and not app_name:
            raise ValueError("Either app_id or app_name should be provided")

        if not app_id:
            apps = self.app_list(header_id, folder_id)
            for app in apps:
                if app["title"].lower() == app_name.lower():
                    app_id = app["id"]
                    break

        if not app_id:
            raise ValueError(f"App with name {app_name} not found")

        return self.client.raw_api.get(
            f"{self.master_folder}/Page?headerId={header_id}&pageId={app_id}"
        )

    def app_form_update(self, header_id: str, app_id: str, fields):
        """Updates form application
        :header_id: ID of the style, material, etc
        :app_id: ID of the application / page
        :fields: Dictionary of fields to update {'field_id':'value'}
        """
        return self.client.raw_api.post(
            f"{self.master_folder}/PageForm?headerId={header_id}&pageId={app_id}",
            body=[{"id": field_id, "value": fields[field_id]} for field_id in fields],
        )

    def app_grid_update(self, header_id: str, app_id: str, rows):
        """Updates form application
        :header_id: ID of the style, material, etc
        :app_id: ID of the application / page
        :rows: List of row dictionaries
        """
        return self.client.raw_api.post(
            f"{self.master_folder}/PageGrid?headerId={header_id}&pageId={app_id}",
            body=rows,
        )

    def app_list_update(self, header_id: str, app_id: str, list_items):
        """Updates List application
        :header_id: ID of the style, material, etc
        :app_id: ID of the application / page
        :list_items: Items of the list app
        """
        return self.client.raw_api.post(
            f"{self.master_folder}/PageList?headerId={header_id}&pageId={app_id}",
            body=list_items,
        )

    def app_attachments_delete(self, header_id: str, app_id: str, filenames_to_remove):
        """Deletes files from Attachments app
        :header_id: ID of the style, material, etc
        :app_id: ID of the application / page
        :filenames_to_remove: List of filenames to be removed
        """
        return self.client.raw_api.post(
            f"{self.master_folder}/AttachmentRemove?headerId={header_id}&pageId={app_id}",
            body=filenames_to_remove,
        )
