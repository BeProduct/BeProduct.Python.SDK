"""
File: _common_tags_async.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: Common Tags Mixin - Async Version
"""

from .sdk_async import BeProductAsync

class TagsMixinAsync:
    """
    Common tags methods for any master folder (Style, Material, etc.) - Async Version
    """

    def __init__(self, client: BeProductAsync):
        self.client = client

    async def tags_list(self, header_id: str):
        """Returns list of tags asynchronously

        :header_id: ID of the style, material, etc
        :returns: List of tags

        """
        return await self.client.raw_api.get(
            f"{self.master_folder}/Tags?headerId={header_id}")

    async def tags_add(self, header_id: str, tag: str):
        """Adds new tag asynchronously

        :header_id: ID of the style, material, etc
        :tag: Tag to add
        :returns: None

        """
        return await self.client.raw_api.post(
            f"{self.master_folder}/Tags/Add?headerId={header_id}",
            body=tag)

    async def tags_delete(self, header_id: str, tag: str):
        """Deletes tag asynchronously

        :header_id: ID of the style, material, etc
        :tag: Tag to delete
        :returns: None

        """
        return await self.client.raw_api.post(
            f"{self.master_folder}/Tags/Delete?headerId={header_id}",
            body=tag)

    async def tag_list(self):
        """List of Style/Material/Image/Color tags asynchronously

        :returns: List of tags

        """
        return await self.client.raw_api.get(
            f"Tag/{self.master_folder}/List")

    async def tag_create(self, name: str, integration: str = None, share_with=None):
        """Creates new tag asynchronously

        :name: Tag name
        :integration: 'Browzwear' if needs to be integrated with Browzwear otherwise none
        :share_with: List of user IDs
        :returns: Created tag

        """
        return await self.client.raw_api.post(
            f"Tag/{self.master_folder}/Create",
            body={
                'name': name,
                'integration': integration,
                'shareWith': share_with if share_with else []
            }
        )

    async def tag_update(self, tag_id: str, name: str, integration: str = None):
        """Updates a tag asynchronously

        :tag_id: Tag ID
        :name: Tag name
        :integration: 'Browzwear' if needs to be integrated with Browzwear otherwise none
        :returns: Updated tag

        """
        return await self.client.raw_api.post(
            f"Tag/{tag_id}/Update",
            body={
                'name': name,
                'integration': integration,
            }
        )

    async def tag_share(self, tag_id: str, share_with):
        """Shares a tag asynchronously

        :tag_id: Tag ID
        :share_with: List of User IDs to share with
        :returns: None

        """
        return await self.client.raw_api.post(
            f"Tag/{tag_id}/Share",
            body=share_with
        )

    async def tag_unshare(self, tag_id: str, unshare_with):
        """Unshares a tag asynchronously

        :tag_id: Tag ID
        :unshare_with: List of User IDs to unshare with
        :returns: None

        """
        return await self.client.raw_api.post(
            f"Tag/{tag_id}/Unshare",
            body=unshare_with
        )

    async def tag_delete(self, tag_id: str):
        """Deletes a tag asynchronously

        :tag_id: Tag ID
        :returns: None

        """
        return await self.client.raw_api.delete(f"Tag/{tag_id}/Delete")

    async def attributes_tag_list(self, header_id: str):
        """List of Style/Material/Image/Color tags asynchronously

        :header_id: ID of the style, material, image etc.
        :returns: List of tags

        """
        return await self.client.raw_api.get(f"Tag/Header/{header_id}")

    async def attributes_tag_add(self, header_id: str, tag_names):
        """Adds tags to the Attributes app asynchronously

        :header_id: ID of the style, material, image etc.
        :tag_names: List of strings (tag names)
        :returns: None

        """
        return await self.client.raw_api.post(
            f"Tag/Header/{header_id}/Add",
            body=tag_names
        )

    async def attributes_tag_remove(self, header_id: str, tag_names):
        """Remove tags from the Attributes app asynchronously

        :header_id: ID of the style, material, image etc.
        :tag_names: List of strings (tag names)
        :returns: None

        """
        return await self.client.raw_api.post(
            f"Tag/Header/{header_id}/Remove",
            body=tag_names
        ) 