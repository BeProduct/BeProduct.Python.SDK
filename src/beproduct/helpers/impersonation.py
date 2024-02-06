"""
File: impersonation.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: BeProduct Helpers for Impersonation
"""

import os
import datetime
import time
import json
from beproduct.sdk import BeProduct
from beproduct.auth import OAuth2Client


def impersonated(
    client: BeProduct,
    *,
    user_id,
    impersonation_client_id=None,
    impersonation_client_secret=None
) -> BeProduct:

    """
    Returns new client that impersonates a different user.
    Impersonating user must be an admin in the company where
    impersonated user registered as a PRIVATE user.
    """

    def _get_access_token(self):
        if not self.access_token or self.token_expires < time.time():
            self.request_token(
                grant_type="refresh_token", refresh_token=self.refresh_token,
            )
            if hasattr(self, "impersonate_userid") and self.impersonate_userid:
                request = {
                    "client_id": impersonation_client_id
                    or os.environ["BEPRODUCT_IMPERSONATION_CLIENT_ID"],
                    "client_secret": impersonation_client_secret
                    or os.environ["BEPRODUCT_IMPERSONATION_SECRET"],
                    "grant_type": "actas",
                    "token": self.access_token,
                    "actas": self.impersonate_userid,
                    "scope": "openid profile email roles offline_access BeProductPublicApi",
                }

                import urllib

                msg = urllib.request.urlopen(
                    self.token_endpoint,
                    urllib.parse.urlencode(request).encode("utf-8"),
                )
                data = json.loads(
                    msg.read().decode(msg.info().get_content_charset() or "utf-8")
                )

                self.access_token = data["access_token"]
                self.expires_in = data["expires_in"]

                if "expires_in" in data:
                    seconds = int(self.expires_in)
                    self.token_expires = (
                        time.mktime(
                            (
                                datetime.datetime.utcnow()
                                + datetime.timedelta(seconds=seconds)
                            ).timetuple()
                        )
                        - 300.0
                    )  # 5 min before

        return self.access_token

    if not user_id:
        raise ValueError("user_id must be provided")

    impersonated_client = BeProduct(
        client_id=client.oauth2_client.client_id,
        client_secret=client.oauth2_client.client_secret,
        refresh_token=client.oauth2_client.refresh_token,
        token_endpoint=client.oauth2_client.token_endpoint,
        company_domain=client.company_domain,
    )

    impersonated_client.public_api_url = client.public_api_url
    impersonated_client.automation_api_url = client.automation_api_url

    impersonated_client.oauth2_client.get_access_token = _get_access_token.__get__(
        impersonated_client.oauth2_client, OAuth2Client
    )
    impersonated_client.oauth2_client.impersonate_userid = user_id
    return impersonated_client
