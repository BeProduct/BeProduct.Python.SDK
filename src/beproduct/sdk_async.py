"""
File: sdk_async.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: Async BeProduct Public API SDK Wrapper
"""

from typing import Optional
from beproduct.auth_async import OAuth2ClientAsync


class BeProductAsync:
    """
    Async BeProduct Public API Client
    """

    def __init__(
        self,
        company_domain: str,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        refresh_token: Optional[str] = None,
        access_token: Optional[str] = None,
        token_endpoint: str = "https://id.winks.io/ids/connect/token",
        public_api_url: str = "https://developers.beproduct.com",
        automation_api_url: str = "https://automation.beproduct.com",
    ):
        """Async BeProduct Public API Client

        Args:
            company_domain: BeProduct customer domain identifier
            client_id: Client ID for OAuth2 authentication
            client_secret: Client secret for OAuth2 authentication
            refresh_token: OAuth2 refresh token
            access_token: Direct bearer token for authentication
            token_endpoint: OAuth2 token endpoint URL
            public_api_url: BeProduct public API URL
            automation_api_url: BeProduct Automation URL

        Returns:
            Async Public API client instance

        Note:
            Either provide OAuth2 credentials (client_id, client_secret, refresh_token)
            OR provide a direct access_token. Do not provide both.
        """
        self.public_api_url = f"{public_api_url.rstrip('/')}/api/{company_domain}"
        self.automation_api_url = f"{automation_api_url.rstrip('/')}/api"
        self.company_domain = company_domain

        # Set up authentication
        if access_token:
            if any([client_id, client_secret, refresh_token]):
                raise ValueError("Cannot provide both access_token and OAuth2 credentials")
            self.oauth2_client = None
            self.access_token = access_token
        else:
            if not all([client_id, client_secret, refresh_token]):
                raise ValueError("Must provide all OAuth2 credentials (client_id, client_secret, refresh_token) or access_token")
            self.oauth2_client = OAuth2ClientAsync(
                token_endpoint=token_endpoint,
                client_id=client_id,
                client_secret=client_secret,
            )
            self.oauth2_client.refresh_token = refresh_token
            self.access_token = None
        
        # Initialize raw API first since other components depend on it
        from ._raw_api_async import RawApiAsync
        self.raw_api = RawApiAsync(self)

        from ._style_async import StyleAsync
        from ._material_async import MaterialAsync
        from ._image_async import ImageAsync
        from ._color_async import ColorAsync
        from ._block_async import BlockAsync
        from ._directory_async import DirectoryAsync
        from ._user_async import UserAsync
        from ._tracking_async import TrackingAsync
        from ._automation_async import AutomationAsync
        from ._schema_async import SchemaAsync

        # Initialize API handlers
        self.style = StyleAsync(self)
        self.material = MaterialAsync(self)
        self.image = ImageAsync(self)
        self.color = ColorAsync(self)
        self.block = BlockAsync(self)
        self.directory = DirectoryAsync(self)
        self.user = UserAsync(self)
        self.tracking = TrackingAsync(self)
        self.automation = AutomationAsync(self)
        self.schema = SchemaAsync(self)

    async def __aenter__(self):
        """Async context manager entry

        Returns:
            Self instance
        """
        # Ensure raw API session is initialized
        await self.raw_api.ensure_session()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit - ensures resources are properly closed

        Args:
            exc_type: Exception type if an error occurred
            exc_val: Exception value if an error occurred
            exc_tb: Exception traceback if an error occurred
        """
        if hasattr(self, 'raw_api'):
            await self.raw_api.close_session() 