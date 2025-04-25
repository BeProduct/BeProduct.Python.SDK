"""
File: _automation_async.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: Async implementation of BeProduct Automation API
"""

import json
from typing import Dict, Any, Optional, List
import os
import aiohttp
import time
import logging

from ._exception import BeProductException
from .sdk_async import BeProductAsync


class AutomationAsync:
    """Automation API class - Async Version"""

    def __init__(self, client: BeProductAsync):
        self.client = client
        self._session = None

    async def ensure_session(self):
        """Ensures aiohttp session exists"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()

    async def close_session(self):
        """Closes aiohttp session if it exists"""
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None

    def __get_headers(self):
        return {
            "X-Authorization": f"Bearer {self.client.oauth2_client.get_access_token()}",
            "Content-type": "application/json",
        }

    async def get(self, url):
        """GET Request to BeProduct Automation API asynchronously

        :url: url to call
        :returns: response body as string or throws an error
        """
        await self.ensure_session()
        full_url = f"{self.client.automation_api_url}/{url.lstrip('/')}"
        
        async with self._session.get(url=full_url, headers=self.__get_headers()) as response:
            if response.status != 200:
                raise BeProductException(
                    "Automation API call failed. Details: \n"
                    + f"URL: {full_url} \n"
                    + f"Status code: {response.status} \n"
                    + f"Response body: {await response.text()} \n"
                )
            
            return await response.json()

    async def delete(self, url):
        """DELETE Request to BeProduct Automation API asynchronously

        :url: url to call
        :returns: response body as string or throws an error
        """
        await self.ensure_session()
        full_url = f"{self.client.automation_api_url}/{url.lstrip('/')}"
        
        async with self._session.delete(url=full_url, headers=self.__get_headers()) as response:
            if response.status != 200:
                raise BeProductException(
                    "Automation API call failed. Details: \n"
                    + f"URL: {full_url} \n"
                    + f"Status code: {response.status} \n"
                    + f"Response body: {await response.text()} \n"
                )
            
            return await response.json()

    async def post(self, url, body):
        """POST Request to BeProduct Automation API asynchronously

        :url: api url
        :body: json body
        :returns: response body as string or throws an error
        """
        await self.ensure_session()
        full_url = f"{self.client.automation_api_url}/{url.lstrip('/')}"
        
        async with self._session.post(url=full_url, json=body, headers=self.__get_headers()) as response:
            if response.status != 200:
                raise BeProductException(
                    "Automation API POST call failed. Details:\n"
                    + f"URL: {full_url} \n"
                    + f"Body: {json.dumps(body)} \n"
                    + f"Status code: {response.status} \n"
                    + f"Response body: {await response.text()} \n"
                )
            
            return await response.json()

    async def autonumber_generate(self, id: str):
        """Generates autonumber defined in Automation asynchronously"""
        result = await self.get(
            f"autonumber?id={id}&company=" + f"{self.client.company_domain}"
        )
        return result["generatedNumber"]

    async def autonumber_list(self, name: str = ""):
        """Get autonumber list asynchronously (filter by name if requested)"""
        result = await self.get(
            f"autonumber-list?name={name}&company=" + f"{self.client.company_domain}"
        )
        return result["autonumbers"]

    async def autonumber_create(self, name: str, template="[00000]"):
        """Creates new autonumber generator asynchronously"""
        return await self.post(
            f"autonumber?name={name}&company=" + f"{self.client.company_domain}",
            {"name": name, "template": template},
        )

    async def lock_aquire(self, name: str, timeout: int = 60):
        """Acquire lock by name asynchronously"""
        return await self.get(
            f"locks?name={name}&timeout={timeout}&company=" + self.client.company_domain
        )

    async def lock_release(self, name: str):
        """Release lock by name asynchronously"""
        return await self.delete(f"locks?name={name}&company=" + self.client.company_domain)

    async def lock_check(self, names: list, timeout: int):
        """Check if locks are acquired asynchronously"""
        return await self.post(
            f"locks?timeout={timeout}&company=" + self.client.company_domain, body=names
        ) 