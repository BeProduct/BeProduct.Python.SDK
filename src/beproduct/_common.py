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

    def folders(self):
        """
        :returns: List of folders
        """
        return self.client.raw_api.get(f"{self.master_folder}/Folders")

    def attributes_list(
            self,
            folder_id: str = "",
            filters=None,
            colorway_filters=None,
            page_size=30):
        """
        :folder_id: Folder ID
        :filters: List of filter dictionaries
        :colorway_filters: List of colorway filter dictionaries
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

        while True:
            page = get_batch(self, folder_id, page_size, page_number)
            total = page['total']

            for attr in page['result']:
                processed += 1
                yield attr

            if processed >= total:
                break

            page_number += 1

    def attributes_get(self, header_id: str):
        """Returns style attibutes

        :header_id: ID of the style, material, image etc.
        :returns: dictionary of the requested style attributes

        """
        return self.client.raw_api.get(f"{self.master_folder}/Header/{header_id}")

    def attributes_delete(self, header_id: str):
        """Deletes Style/Material/Image by ID

        :header_id: ID of the Style/Material/Image
        :returns:

        """
        return self.client.raw_api.get(
                f"{self.master_folder}/Header/Delete/{header_id}")

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
        :fields: List of row dictionaries
        """
        return self.client.raw_api.post(
            f"{self.master_folder}/PageGrid?headerId={header_id}&pageId={app_id}",
            body=rows)

    def attributes_share(self, header_id: str, partner_list):
        """Shares attributes page

        :header_id: ID of style/material/image etc
        :partner_list: list of partner IDs

        """
        return self.client.raw_api.post(
            f"Share/Header/{header_id}/Share",
            body=partner_list
        )

    def app_share(self, header_id: str, app_id: str, partner_list):
        """Shares application

        :header_id: ID of style/material/image etc
        :app_id: ID of the application
        :partner_list: list of partner IDs

        """
        return self.client.raw_api.post(
            f"Share/Page/{header_id}/{app_id}/Share",
            body=partner_list
        )

    def attributes_unshare(self, header_id: str, partner_list):
        """Unshares attributes page

        :header_id: ID of style/material/image etc
        :partner_list: list of partner IDs

        """
        return self.client.raw_api.post(
            f"Share/Header/{header_id}/Unshare",
            body=partner_list
        )

    def app_unshare(self, header_id: str, app_id: str, partner_list):
        """Shares application

        :header_id: ID of style/material/image etc
        :app_id: ID of the application
        :partner_list: list of partner IDs

        """
        return self.client.raw_api.post(
            f"Share/Page/{header_id}/{app_id}/Unshare",
            body=partner_list
        )

    def attributes_shared_with(self, header_id: str):
        """ Gets list of all partners with whom
            attributes page is shared

        :header_id: ID of style/material/image etc
        :returns: List of partners

        """
        return self.client.raw_api.get(f"Share/Header/{header_id}/Get")

    def app_shared_with(self, header_id: str, app_id: str):
        """ Gets list of all partners with whom
            app is shared

        :header_id: ID of style/material/image etc
        :app_id: ID of the application
        :returns: List of partners

        """
        return self.client.raw_api.get(f"Share/Page/{header_id}/{app_id}/Get")
