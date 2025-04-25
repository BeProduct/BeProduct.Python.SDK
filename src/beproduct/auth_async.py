"""
File: _auth_async.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: BeProduct Public API OAuth2 client - Async Version
"""

import aiohttp
import json
from datetime import datetime, timedelta
from time import mktime
from urllib.parse import urlencode, parse_qsl
import asyncio
from typing import Dict, Any, Optional

class OAuth2ClientAsync:
    """OAuth 2.0 client object - Async Version"""

    def __init__(
        self,
        auth_endpoint=None,
        token_endpoint=None,
        client_id=None,
        client_secret=None,
    ):
        """Instantiates a `OAuth2ClientAsync` to authorize and authenticate a user
        :param auth_endpoint: The authorization endpoint as issued by the
                              provider. This is where the user should be
                              redirect to provider authorization for your
                              application.
        :param token_endpoint: The endpoint against which a `code` will be
                               exchanged for an access token.
        :param client_id: The client ID as issued by the provider.
        :param client_secret: The client secret as issued by the provider. This
                              must not be shared.
        """
        self.auth_endpoint = auth_endpoint
        self.token_endpoint = token_endpoint
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.token_expires = -1
        self.refresh_token = None
        self._lock = asyncio.Lock()  # Thread-safe token refresh

    def auth_uri(
        self, redirect_uri=None, scope=None, scope_delim=None, state=None, **kwargs
    ):
        """Builds the auth URI for the authorization endpoint
        :param scope: (optional) The `scope` parameter to pass for
                      authorization. The format should match that expected by
                      the provider
        :param state: (optional) The `state` parameter to pass for
                      authorization. If the provider follows the OAuth 2.0
                      spec, this will be returned to your `redirect_uri` after
                      authorization. Generally used for CSRF protection.
        :param **kwargs: Any other querystring parameters to be passed to the
                         provider.
        """
        kwargs.update(
            {
                "client_id": self.client_id,
                "response_type": "code",
            }
        )

        if scope is not None:
            kwargs["scope"] = scope

        if state is not None:
            kwargs["state"] = state

        if redirect_uri is not None:
            kwargs["redirect_uri"] = redirect_uri

        return f"{self.auth_endpoint}?{urlencode(kwargs)}"

    async def request_token(self, parser=None, redirect_uri=None, **kwargs):
        """Request an access token from the token endpoint asynchronously.
        This is largely a helper method and expects the client code to
        understand what the server expects. Anything that's passed into
        ``**kwargs`` will be sent (``urlencode``d) to the endpoint. Client
        secret and client ID are automatically included, so are not required
        as kwargs.
        
        :param parser: Callback to deal with returned data. Not all providers
                       use JSON.
        :param redirect_uri: The redirect URI used in the auth flow
        :param **kwargs: Additional parameters to pass to the token endpoint
        """
        kwargs = kwargs or {}
        
        parser = parser or _default_parser
        kwargs.update(
            {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "grant_type" in kwargs
                and kwargs["grant_type"]
                or "authorization_code",
            }
        )

        if redirect_uri is not None:
            kwargs["redirect_uri"] = redirect_uri

        async with aiohttp.ClientSession() as session:
            async with session.post(self.token_endpoint, data=kwargs) as response:
                if response.status != 200:
                    response_text = await response.text()
                    raise Exception(f"Token request failed: {response.status}, {response_text}")
                
                data = parser(await response.text())
                
                for key in data:
                    setattr(self, key, data[key])

                # expires_in is RFC-compliant. if anything else is used by the
                # provider, token_expires must be set manually
                if hasattr(self, "expires_in"):
                    seconds = int(self.expires_in)
                    self.token_expires = (
                        mktime((datetime.utcnow() + timedelta(seconds=seconds)).timetuple())
                        - 300.0
                    )  # 5 min before

    async def refresh(self):
        """Refresh the access token using the refresh token"""
        await self.request_token(refresh_token=self.refresh_token, grant_type="refresh_token")

    async def get_access_token(self):
        """Returns access token
        Autorefresh is performed if necessary

        :returns: Access token
        """
        async with self._lock:
            if not self.access_token or self.token_expires < mktime(
                datetime.utcnow().timetuple()
            ):
                await self.request_token(
                    grant_type="refresh_token", refresh_token=self.refresh_token
                )

            return self.access_token


def _default_parser(data):
    """Default parser that attempts to parse JSON, falling back to query string parsing"""
    try:
        return json.loads(data)
    except ValueError:
        return dict(parse_qsl(data)) 