"""
File: _common_attributes.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: Attributes Mixin for every master folder
"""

from ._helpers import beproduct_paging_iterator


class AttributesMixin:
    """
    Attributes mixin class for every master folder
    """

    def folders(self):
        """
        :returns: List of folders
        """
        return self.client.raw_api.get(f"{self.master_folder}/Folders")

    def folder_schema(self, folder_id: str):
        """Gets attributes schema (list of fields ) for a folder

        :folder_id: ID of the folder
        :returns: Attributes schema

        """
        return self.client.raw_api.get(
            f"{self.master_folder}/FolderSchema?folderId={folder_id}")

    # ATTRIBUTES

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

        return beproduct_paging_iterator(
            page_size,
            lambda psize, pnum: self.client.raw_api.post(
                f"{self.master_folder}/Headers?folderId={folder_id}" +
                f"&pageSize={psize}&pageNumber={pnum}",
                body={
                    'filters':  filters,
                    'colorwayFilters': colorway_filters
                }))

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
