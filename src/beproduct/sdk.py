"""
File: sdk.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: BeProduct Public API SDK Wrapper
"""

import json
import requests
from .auth import OAuth2Client


class BeProductException(Exception):
    """
    BeProduct Custom Exception
    """
    pass


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

    def __get_headers(self):
        return {
            'Authorization': f'Bearer {self.oauth2_client.get_access_token()}',
            'Content-type': 'application/json',
        }

    def get(self, url):
        """ Get Request to BeProduct Public API

        :url: url to call
        :returns: response body as string or throws an error

        """
        full_url = f"{self.public_api_url}/{url.lstrip('/')}"
        response = requests.get(
            url=full_url,
            headers=self.__get_headers())

        if response.status_code != 200:
            raise BeProductException(
                "API call failed. Details: \n" +
                f"URL: {full_url} \n" +
                f"Status code: {response.status_code} \n" +
                f"Response body: {response.text} \n")

        return response.json()

    def post(self, url, body):
        """ Post Request to BeProduct Public API

        :url: papi url
        :body: json body
        :returns: response body as string or throws an error

        """
        full_url = f"{self.public_api_url}/{url.lstrip('/')}"
        response = requests.post(
            url=full_url,
            json=body,
            headers=self.__get_headers())

        if response.status_code != 200:
            raise BeProductException(
                "PAPI POST call failed. Details:\n" +
                f"URL: {full_url} \n" +
                f"Body: {json.dumps(body)} \n" +
                f"Status code: {response.status_code} \n" +
                f"Response body: {response.text} \n")

        return response.json()

    # ### Public API METHODS ###
    from ._style import style_attributes_get
    from ._style import style_attributes_update
