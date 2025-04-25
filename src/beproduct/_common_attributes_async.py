"""
File: _common_attributes_async.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: Common Attributes Mixin - Async Version
"""

from ._helpers_async import beproduct_paging_iterator_async
from .sdk_async import BeProductAsync

class AttributesMixinAsync:
    """
    Common attributes methods for any master folder (Style, Material, etc.) - Async Version
    """

    def __init__(self, client: BeProductAsync):
        self.client = client

    def attributes_list(self, folder_id: str = None, filters=None):
        """Returns list of attributes asynchronously

        :folder_id: ID of the folder to list attributes from
        :filters: List of filters to apply
        :returns: Async iterator of attributes

        """
        async def get_page(psize, pnum):
            return await self.client.raw_api.post(
                f"{self.master_folder}/Headers?folderId={folder_id}" +
                f"&pageSize={psize}&pageNumber={pnum}",
                body={
                    'filters': filters,
                    'colorwayFilters': []
                })

        return beproduct_paging_iterator_async(30, get_page)

    async def attributes_get(self, header_id: str):
        """Returns attributes by ID asynchronously

        :header_id: ID of the attributes
        :returns: Dictionary of the requested attributes

        """
        return await self.client.raw_api.get(
            f"{self.master_folder}/Header/{header_id}")

    async def attributes_delete(self, header_id: str):
        """Deletes attributes by ID asynchronously

        :header_id: ID of the attributes
        :returns: None

        """
        return await self.client.raw_api.post(
            f"{self.master_folder}/Header/{header_id}/Delete")

    async def folders(self):
        """
        :returns: List of folders
        """
        return await self.client.raw_api.get(f"{self.master_folder}/Folders")

    async def folder_schema(self, folder_id: str):
        """Gets attributes schema (list of fields ) for a folder

        :folder_id: ID of the folder
        :returns: Attributes schema

        """
        return await self.client.raw_api.get(
            f"{self.master_folder}/FolderSchema?folderId={folder_id}"
        )

    async def attributes_get_by_number(self, header_number: str, **kwargs):
        """Returns style attibutes by number

        :header_number: Number of the style, material, image etc.
        :**kwargs: Additional url parameters
        :returns: dictionary of the requested style attributes
        """
        async for item in self.attributes_list(
            filters=[
                {"field": "header_number", "operator": "Eq", "value": header_number}
            ]
        ):
            return item
        return None 