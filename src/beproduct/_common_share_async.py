"""
File: _common_share_async.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: Common Share Mixin - Async Version
"""

from .sdk_async import BeProductAsync

class ShareMixinAsync:
    """
    Common share methods for any master folder (Style, Material, etc.) - Async Version
    """

    def __init__(self, client: BeProductAsync):
        self.client = client

    async def share_list(self, header_id: str):
        """Returns list of shares asynchronously

        :header_id: ID of the style, material, etc
        :returns: List of shares

        """
        return await self.client.raw_api.get(
            f"{self.master_folder}/Share?headerId={header_id}")

    async def share_create(self, header_id: str, email: str, role: str = None):
        """Creates new share asynchronously

        :header_id: ID of the style, material, etc
        :email: Email to share with
        :role: Role to assign
        :returns: Created share

        """
        return await self.client.raw_api.post(
            f"{self.master_folder}/Share/Create?headerId={header_id}" +
            f"&email={email}" +
            (f"&role={role}" if role else ""))

    async def share_delete(self, header_id: str, share_id: str):
        """Deletes share asynchronously

        :header_id: ID of the style, material, etc
        :share_id: ID of the share
        :returns: None

        """
        return await self.client.raw_api.post(
            f"{self.master_folder}/Share/Delete?headerId={header_id}" +
            f"&shareId={share_id}")

    async def share_update(self, header_id: str, share_id: str, role: str):
        """Updates share asynchronously

        :header_id: ID of the style, material, etc
        :share_id: ID of the share
        :role: New role to assign
        :returns: Updated share

        """
        return await self.client.raw_api.post(
            f"{self.master_folder}/Share/Update?headerId={header_id}" +
            f"&shareId={share_id}&role={role}")

    async def attributes_share(self, header_id: str, partner_list):
        """Shares attributes page asynchronously

        :header_id: ID of style/material/image etc
        :partner_list: List of partner IDs
        :returns: None

        """
        return await self.client.raw_api.post(
            f"Share/Header/{header_id}/Share",
            body=partner_list
        )

    async def app_share(self, header_id: str, app_id: str, partner_list):
        """Shares application asynchronously

        :header_id: ID of style/material/image etc
        :app_id: ID of the application
        :partner_list: List of partner IDs
        :returns: None

        """
        return await self.client.raw_api.post(
            f"Share/Page/{header_id}/{app_id}/Share",
            body=partner_list
        )

    async def attributes_unshare(self, header_id: str, partner_list):
        """Unshares attributes page asynchronously

        :header_id: ID of style/material/image etc
        :partner_list: List of partner IDs
        :returns: None

        """
        return await self.client.raw_api.post(
            f"Share/Header/{header_id}/Unshare",
            body=partner_list
        )

    async def app_unshare(self, header_id: str, app_id: str, partner_list):
        """Unshares application asynchronously

        :header_id: ID of style/material/image etc
        :app_id: ID of the application
        :partner_list: List of partner IDs
        :returns: None

        """
        return await self.client.raw_api.post(
            f"Share/Page/{header_id}/{app_id}/Unshare",
            body=partner_list
        )

    async def attributes_shared_with(self, header_id: str):
        """Gets list of all partners with whom attributes page is shared asynchronously

        :header_id: ID of style/material/image etc
        :returns: List of partners

        """
        return await self.client.raw_api.get(f"Share/Header/{header_id}/Get")

    async def app_shared_with(self, header_id: str, app_id: str):
        """Gets list of all partners with whom app is shared asynchronously

        :header_id: ID of style/material/image etc
        :app_id: ID of the application
        :returns: List of partners

        """
        return await self.client.raw_api.get(f"Share/Page/{header_id}/{app_id}/Get") 