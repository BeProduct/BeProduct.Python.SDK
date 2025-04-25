"""
File: _raw_api_async.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: Async Raw API class
"""

import json
import os
import aiohttp
import asyncio
import logging
from typing import Dict, Any, Optional, Tuple

from ._exception import BeProductException
from ._encoder import MultipartEncoder, FileFromURLWrapper
from .sdk_async import BeProductAsync


class ThrottleAsync:
    """Implements async throttling policy"""

    def __init__(self, strategy=None):
        """Constructor"""
        self.strategy = strategy or [1, 3, 5, 15, 30]  # seconds to wait
        self.current = 0  # index in strategy

    async def wait_or_die(self) -> bool:
        """Used to retry api calls asynchronously
        :returns: True if waited, False not going to wait anymore
        """
        if len(self.strategy) <= self.current:
            return False

        logging.info(f"Throttling. Waiting {self.strategy[self.current]} sec.")
        await asyncio.sleep(self.strategy[self.current])

        self.current += 1
        return True


class RawApiAsync:
    """Async Raw API class"""

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

    def __append_url_parameters(self, url: str, param_dict: Dict) -> str:
        """Appends URL parameters to the URL"""
        if param_dict:
            result_url = url
            result_url += "?" if "?" not in url else "&"
            result_url += "&".join(
                [f"{key}={value}" for key, value in param_dict.items()]
            )
            return result_url
        return url

    async def __get_headers(self):
        """Gets headers for API requests including auth"""
        return {
            "Authorization": f"Bearer {await self.__get_token()}",
            "Content-type": "application/json",
        }

    async def __get_auth_header(self):
        """Gets auth header only"""
        return {
            "Authorization": f"Bearer {await self.__get_token()}"
        }

    async def __get_token(self) -> str:
        """Gets the appropriate token based on authentication method"""
        if self.client.oauth2_client:
            return await self.client.oauth2_client.get_access_token()
        return self.client.access_token

    async def get(self, url: str, **kwargs):
        """GET Request to BeProduct Public API
        :url: url to call
        :returns: response body as string or throws an error
        """
        throttle = ThrottleAsync()
        full_url = self.__append_url_parameters(
            f"{self.client.public_api_url}/{url.lstrip('/')}", kwargs
        )

        await self.ensure_session()
        headers = await self.__get_headers()

        while True:
            async with self._session.get(url=full_url, headers=headers) as response:
                if response.status == 429 and await throttle.wait_or_die():
                    continue

                if response.status == 401:
                    if self.client.oauth2_client:
                        # Only retry with OAuth2 client
                        headers = await self.__get_headers()  # Refresh token and try again
                        continue
                    error_text = await response.text()
                    raise BeProductException(
                        "Authentication failed. Token may be expired or invalid.\n"
                        + f"Status code: {response.status} \n"
                        + f"Response body: {error_text} \n"
                    )

                if response.status != 200:
                    error_text = await response.text()
                    raise BeProductException(
                        "API call failed. Details: \n"
                        + f"URL: {full_url} \n"
                        + f"Status code: {response.status} \n"
                        + f"Response body: {error_text} \n"
                    )

                return await response.json()

    async def delete(self, url: str, **kwargs) -> Dict[str, Any]:
        """DELETE Request to BeProduct Public API
        :url: url to call
        :returns: response body as string or throws an error
        """
        throttle = ThrottleAsync()
        full_url = self.__append_url_parameters(
            f"{self.client.public_api_url}/{url.lstrip('/')}", kwargs
        )

        await self.ensure_session()
        headers = await self.__get_headers()

        while True:
            async with self._session.delete(url=full_url, headers=headers) as response:
                if response.status == 429 and await throttle.wait_or_die():
                    continue

                if response.status == 401:
                    if self.client.oauth2_client:
                        # Only retry with OAuth2 client
                        headers = await self.__get_headers()  # Refresh token and try again
                        continue
                    error_text = await response.text()
                    raise BeProductException(
                        "Authentication failed. Token may be expired or invalid.\n"
                        + f"Status code: {response.status} \n"
                        + f"Response body: {error_text} \n"
                    )

                if response.status != 200:
                    error_text = await response.text()
                    raise BeProductException(
                        "API call failed. Details: \n"
                        + f"URL: {full_url} \n"
                        + f"Status code: {response.status} \n"
                        + f"Response body: {error_text} \n"
                    )

                return await response.json()

    async def post(self, url: str, body: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """POST Request to BeProduct Public API
        :url: api url
        :body: json body
        :returns: response body as string or throws an error
        """
        throttle = ThrottleAsync()
        full_url = self.__append_url_parameters(
            f"{self.client.public_api_url}/{url.lstrip('/')}", kwargs
        )

        await self.ensure_session()
        headers = await self.__get_headers()

        while True:
            async with self._session.post(url=full_url, json=body, headers=headers) as response:
                if response.status == 429 and await throttle.wait_or_die():
                    continue

                if response.status == 401:
                    if self.client.oauth2_client:
                        # Only retry with OAuth2 client
                        headers = await self.__get_headers()  # Refresh token and try again
                        continue
                    error_text = await response.text()
                    raise BeProductException(
                        "Authentication failed. Token may be expired or invalid.\n"
                        + f"Status code: {response.status} \n"
                        + f"Response body: {error_text} \n"
                    )

                if response.status != 200:
                    error_text = await response.text()
                    raise BeProductException(
                        "API POST call failed. Details:\n"
                        + f"URL: {full_url} \n"
                        + f"Body: {json.dumps(body)} \n"
                        + f"Status code: {response.status} \n"
                        + f"Response body: {error_text} \n"
                    )

                return await response.json()

    async def upload_local_file(self, filepath: str, url: str, body: Optional[Dict[str, Any]] = None, **kwargs) -> str:
        """Uploads a file from the filesystem
        :filepath: path of the file
        :url: api url
        :body: Dict body
        :returns: Upload ID. Check status using upload_completed
        """
        throttle = ThrottleAsync()
        full_url = self.__append_url_parameters(
            f"{self.client.public_api_url}/{url.lstrip('/')}", kwargs
        )

        await self.ensure_session()
        headers = await self.__get_auth_header()

        request_body = {} if body is None else body.copy()
        with open(filepath, "rb") as f:
            request_body["file"] = (
                os.path.basename(filepath),
                f,
                "application/octet-stream",
            )

            data = aiohttp.FormData()
            for key, value in request_body.items():
                if key == "file":
                    data.add_field(key, value[1], filename=value[0], content_type=value[2])
                else:
                    data.add_field(key, str(value))

            while True:
                async with self._session.post(url=full_url, data=data, headers=headers) as response:
                    if response.status == 429 and await throttle.wait_or_die():
                        continue

                    if response.status == 401:
                        if self.client.oauth2_client:
                            # Only retry with OAuth2 client
                            headers = await self.__get_auth_header()  # Refresh token and try again
                            continue
                        error_text = await response.text()
                        raise BeProductException(
                            "Authentication failed. Token may be expired or invalid.\n"
                            + f"Status code: {response.status} \n"
                            + f"Response body: {error_text} \n"
                        )

                    if response.status != 200:
                        error_text = await response.text()
                        raise BeProductException(
                            "API upload call failed. Details:\n"
                            + f"URL: {full_url} \n"
                            + f"Status code: {response.status} \n"
                            + f"Response body: {error_text} \n"
                        )

                    result = await response.json()
                    return result.get("id")

    async def upload_from_url(self, file_url: str, api_url: str, body: Optional[Dict[str, Any]] = None, **kwargs) -> str:
        """Uploads a file from URL to BeProduct Public API
        :file_url: URL of the file to upload
        :api_url: API URL to upload to
        :body: Optional body to include in the request
        :returns: Upload ID
        """
        throttle = ThrottleAsync()
        full_url = self.__append_url_parameters(
            f"{self.client.public_api_url}/{api_url.lstrip('/')}", kwargs
        )

        await self.ensure_session()
        headers = await self.__get_auth_header()

        # First, get the file from the URL using streaming
        async with self._session.get(file_url) as file_response:
            if file_response.status != 200:
                raise BeProductException(
                    f"Failed to download file from {file_url}. Status code: {file_response.status}"
                )

            # Create a multipart encoder with the file data
            encoder = MultipartEncoder(
                fields={
                    "file": ("file", await file_response.read(), file_response.content_type),
                    **(body or {})
                }
            )

            # Update headers with the encoder's content type
            headers["Content-Type"] = encoder.content_type

            # Upload the file
            while True:
                async with self._session.post(url=full_url, data=encoder.to_string(), headers=headers) as response:
                    if response.status == 429 and await throttle.wait_or_die():
                        continue

                    if response.status == 401:
                        if self.client.oauth2_client:
                            # Only retry with OAuth2 client
                            headers = await self.__get_auth_header()  # Refresh token and try again
                            headers["Content-Type"] = encoder.content_type
                            continue
                        error_text = await response.text()
                        raise BeProductException(
                            "Authentication failed. Token may be expired or invalid.\n"
                            + f"Status code: {response.status} \n"
                            + f"Response body: {error_text} \n"
                        )

                    if response.status != 200:
                        error_text = await response.text()
                        raise BeProductException(
                            "API call failed. Details: \n"
                            + f"URL: {full_url} \n"
                            + f"Status code: {response.status} \n"
                            + f"Response body: {error_text} \n"
                        )

                    result = await response.json()
                    # The response might have 'uploadId', 'id', or 'imageId' field
                    upload_id = result.get('uploadId') or result.get('id') or result.get('imageId')
                    if not upload_id:
                        raise BeProductException(
                            "API response missing upload ID. Response: " + str(result)
                        )
                    return upload_id

    async def upload_status(self, file_id: str) -> Tuple[bool, bool, str]:
        """Checks upload status
        :file_id: Upload ID returned by upload_local_file
        :returns: (is_finished, is_error, error_message)
        """
        try:
            # Try new generic upload endpoint first
            result = await self.get(f"upload/{file_id}/status")
            return (
                result.get("isFinished", False),
                result.get("isError", False),
                result.get("errorMessage", ""),
            )
        except BeProductException:
            # Fall back to legacy style endpoint if new one fails
            status = await self.get(f"Style/GetImageProcessingStatus/{file_id}")
            return (
                status.get("finished", False),
                status.get("errorOccured", False),
                status.get("message", ""),
            ) 