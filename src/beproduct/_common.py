"""
File: _common.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: Common Mixin for every master folder
"""


class CommonMixin:
    """
    Common mixin class for every master folder
    """
    def __init__(self, master_folder):
        self.master_folder = master_folder

    def get_folders(self):
        """
        :returns: List of folders
        """
        return self.client.raw_api.get(f"{self.master_folder}/Folders")

    def list(self,
             folder_id: str = "",
             filters=None,
             colorway_filters=None):
        """
        :folder_id: Folder ID
        :filters: List of filter dictionaries
        :returns: Enumerator of Attributes
        """

        def get_batch(self, folder_id, page_size, page_number):
            return self.client.raw_api.post(
                f"{self.master_folder}/Headers?folderId={folder_id}&pageSize={page_size}&pageNumber={page_number}",
                body={ 
                    'filters':  filters,
                    'colorwayFilters': colorway_filters
                })

        total = 0
        processed = 0
        page_number = 0
        page_size = 30

        while True:
            page = get_batch(self, folder_id, page_size, page_number)
            total = page['total']

            for attr in page['result']:
                processed += 1
                yield attr

            if processed >= total:
                break

            page_number += 1

    def get_apps(self, header_id: str):
        """ Returns list of apps/pages
        for a specific style, material, etc

        :header_id: ID of the style, material, etc
        :returns: List of apps
        """
        return self.client.raw_api.get(
            f"{self.master_folder}/Pages?headerId={header_id}")

    def get_pages(self, header_id: str):
        """ Same as get_apps method """
        return self.get_apps(header_id)

    def get_app(self, header_id: str, app_id: str):
        """ Returns a particular app

        :header_id: ID of the style, material, etc
        :app_id: ID of the application / page
        :returns: Dictionary with app data
        """
        return self.client.raw_api.get(f"{self.master_folder}/Page?headerId={header_id}&pageId={app_id}")

    def get_page(self, header_id: str, page_id: str):
        """ Same as get_app """
        return self.get_app(header_id=header_id, app_id=page_id)

    def form_app_update(self, header_id: str, app_id:str, fields):
        """ Updates form application
        :header_id: ID of the style, material, etc
        :app_id: ID of the application / page
        :fields: Dictionary of fields to update {'field_id':'value'}
        """
        return self.client.raw_api.post(
            f"{self.master_folder}/PageForm?headerId={header_id}&pageId={app_id}",
            body=[{'id': field_id, 'value': fields[field_id]} for field_id in fields])
