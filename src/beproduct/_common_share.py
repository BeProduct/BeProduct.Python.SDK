"""
File: _common_share.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: Share Mixin for every master folder
"""


class ShareMixin:

    """
    Share mixin class for every master folder
    """

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
