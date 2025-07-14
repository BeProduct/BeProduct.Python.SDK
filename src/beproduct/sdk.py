"""
File: sdk.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: BeProduct Public API SDK Wrapper
"""

import time
from typing import Dict
from .auth import OAuth2Client


class BeProduct:
    """
    BeProduct Public API Client
    """

    def __init__(
        self,
        client_id: str = None,
        client_secret: str = None,
        refresh_token: str = None,
        company_domain: str = None,
        token_endpoint="https://id.winks.io/ids/connect/token",
        public_api_url="https://developers.beproduct.com",
        automation_api_url="https://automation.beproduct.com",
        access_token: str = None,
        additional_headers: Dict = None,
    ):
        """BeProduct Public API Client

        :client_id: client id
        :client_secret: client sercret
        :refresh_token: refresh_token
        :company_domain: BeProduct customer domain identifier
        :token_endpoint: token endpoint
        :public_api_url: BeProduct public api URL
        :automation_api_url: BeProduct Automation URL
        :returns: Public API client instance

        """
        if not company_domain:
            raise ValueError("company_domain is required")

        if not access_token and not all([client_id, client_secret, refresh_token]):
            raise ValueError(
                "access_token or client_id, client_secret and refresh_token are required"
            )

        self.oauth2_client = OAuth2Client(
            token_endpoint=token_endpoint,
            client_id=client_id,
            client_secret=client_secret,
        )

        if access_token:
            self.oauth2_client.access_token = access_token
            self.oauth2_client.token_expires = (
                time.time() + 3600 * 24
            )  # 1 day, even though access_token has lsmaller ttl

        self.oauth2_client.refresh_token = refresh_token
        self.automation_api_url = f"{automation_api_url.rstrip('/')}/api"
        self.company_domain = company_domain
        self.public_api_url = f"{public_api_url.rstrip('/')}/api/{company_domain}"

        # ### Constructing API handlers ###
        # importing here to prevent cyclic dependency

        from ._raw_api import RawApi

        self.raw_api = RawApi(self, additional_headers=additional_headers)

        from ._style import Style
        from ._image import Image
        from ._material import Material
        from ._color import Color
        from ._block import Block
        from ._directory import Directory
        from ._user import User
        from ._tracking import Tracking
        from ._automation import Automation
        from ._schema import Schema
        from ._helpers import beproduct_paging_iterator_sync

        self.style = Style(self)
        self.image = Image(self)
        self.material = Material(self)
        self.color = Color(self)
        self.block = Block(self)
        self.directory = Directory(self)
        self.user = User(self)
        self.tracking = Tracking(self)
        self.automation = Automation(self)
        self.schema = Schema(self)

        self.beproduct_paging_iterator = beproduct_paging_iterator_sync


class BeProductAsync(BeProduct):
    """
    BeProduct Public API Client Async
    """

    def __init__(self, *args, additional_headers: Dict = None, **kwargs):
        """BeProduct Public API Client Async

        :returns: Public API client instance
        """
        super().__init__(*args, **kwargs)

        # ### Constructing Async API handlers ###

        from ._raw_api_async import RawApiAsync
        from ._helpers import beproduct_paging_iterator_async

        self.raw_api = RawApiAsync(self, additional_headers=additional_headers)
        self.beproduct_paging_iterator = beproduct_paging_iterator_async
