"""
File: _automation.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: Automation API class
"""

import json
from typing import Dict
import os
import requests
import time
import logging


from ._exception import BeProductException
from .sdk import BeProduct


class Automation:
    """Automation API class"""

    def __init__(self, client: BeProduct):
        self.client = client

    def __get_headers(self):
        return {
            "X-Authorization": f"Bearer {self.client.oauth2_client.get_access_token()}",
            "Content-type": "application/json",
        }

    def get(self, url):
        """GET Request to BeProduct Automation API

        :url: url to call
        :returns: response body as string or throws an error

        """
        full_url = f"{self.client.automation_api_url}/{url.lstrip('/')}"
        response = requests.get(url=full_url, headers=self.__get_headers())

        if response.status_code != 200:
            raise BeProductException(
                "Automation API call failed. Details: \n"
                + f"URL: {full_url} \n"
                + f"Status code: {response.status_code} \n"
                + f"Response body: {response.text} \n"
            )

        return response.json()

    def delete(self, url):
        """DELETE Request to BeProduct Automation API

        :url: url to call
        :returns: response body as string or throws an error

        """
        full_url = f"{self.client.automation_api_url}/{url.lstrip('/')}"
        response = requests.delete(url=full_url, headers=self.__get_headers())

        if response.status_code != 200:
            raise BeProductException(
                "Automation API call failed. Details: \n"
                + f"URL: {full_url} \n"
                + f"Status code: {response.status_code} \n"
                + f"Response body: {response.text} \n"
            )

        return response.json()

    def post(self, url, body):
        """POST Request to BeProduct Automation API

        :url: api url
        :body: json body
        :returns: response body as string or throws an error

        """

        full_url = f"{self.client.automation_api_url}/{url.lstrip('/')}"

        response = requests.post(url=full_url, json=body, headers=self.__get_headers())

        if response.status_code != 200:
            raise BeProductException(
                "Automation API POST call failed. Details:\n"
                + f"URL: {full_url} \n"
                + f"Body: {json.dumps(body)} \n"
                + f"Status code: {response.status_code} \n"
                + f"Response body: {response.text} \n"
            )

        return response.json()

    def autonumber_generate(self, id: str):
        """Generates autonumber defined in Automation"""

        return self.get(
            f"autonumber?id={id}&company=" + f"{self.client.company_domain}"
        )["generatedNumber"]

    def autonumber_list(self, name: str = ""):
        """Get autonumber list (filter by name if requested)"""

        return self.get(
            f"autonumber-list?name={name}&company=" + f"{self.client.company_domain}"
        )["autonumbers"]

    def autonumber_create(self, name: str, template="[00000]"):
        """Creates new autonumber generator"""

        return self.post(
            f"autonumber?name={name}&company=" + f"{self.client.company_domain}",
            {"name": name, "template": template},
        )

    def lock_aquire(self, name: str, timeout: int = 60):
        """Acquire lock by name"""
        return self.get(
            f"locks?name={name}&timeout={timeout}&company=" + self.client.company_domain
        )

    def lock_release(self, name: str):
        """Release lock by name"""
        return self.delete(f"locks?name={name}&company=" + self.client.company_domain)
