"""
File: sdk.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: BeProduct Public API SDK Wrapper
"""

from .auth import OAuth2Client


class BeProduct():
    """
    BeProduct Public API Client
    """

    def __init__(self,
                 client_id: str,
                 client_secret: str,
                 refresh_token: str,
                 company_domain: str,
                 token_endpoint="https://id.winks.io/ids/connect/token",
                 public_api_url="https://developers.beproduct.com"):
        """BeProduct Public API Client

        :client_id: client id
        :client_secret: client sercret
        :refresh_token: refresh_token
        :company_domain: BeProduct customer domain identifier
        :token_endpoint: token endpoint
        :public_api_url: BeProduct public api URL
        :returns: Public API client instance

        """
        self.oauth2_client = OAuth2Client(token_endpoint=token_endpoint,
                                          client_id=client_id,
                                          client_secret=client_secret)
        self.oauth2_client.refresh_token = refresh_token
        self.public_api_url = f"{public_api_url.rstrip('/')}/api/{company_domain}"

        # ### Constructing API handlers ###
        # importing here to prevent cyclic dependency

        from ._raw_api import RawApi
        self.raw_api = RawApi(self)

        from ._style import Style
        from ._image import Image
        from ._material import Material
        from ._color import Color
        from ._directory import Directory
        from ._user import User
        from ._tracking import Tracking

        self.style = Style(self)
        self.image = Image(self)
        self.material = Material(self)
        self.color = Color(self)
        self.directory = Directory(self)
        self.user = User(self)
        self.tracking = Tracking(self)
