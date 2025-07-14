"""
File: _upload.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: Raw API class
"""

import json
from typing import Dict
import os
import aiohttp
import asyncio
import time
import logging

from ._exception import BeProductException
from ._encoder import MultipartEncoder, FileFromURLWrapper
from .sdk import BeProduct


class _Throttle:
    """Implements throttling policy"""

    def __init__(self, strategy=None):
        """Constrictor"""
        self.strategy = strategy or [1, 3, 5, 15, 30]  # seconds to wait
        self.current = 0  # index in strategy

    async def wait_or_die(self):
        """Used to retry api calls

        :returns: True if waited, False not going to wait anymore

        """
        if len(self.strategy) <= self.current:
            return False

        logging.info(f"Throttling. Waiting {self.strategy[self.current]} sec.")
        await asyncio.sleep(self.strategy[self.current])

        self.current += 1
        return True


class RawApiAsync:
    """Raw API class"""

    def __init__(self, client: BeProduct, additional_headers: Dict = None):
        self.client = client
        self.logger = logging.getLogger("beproduct.sdk.RawApiAsync")
        self.additional_headers = additional_headers or {}

    def __append_url_parameters(self, url: str, param_dict: Dict):
        if param_dict:
            result_url = url
            result_url += "?" if "?" not in url else "&"
            result_url += "&".join(
                [f"{key}={value}" for key, value in param_dict.items()]
            )
            return result_url
        return url

    def __get_headers(self):
        return {
            "Authorization": f"Bearer {self.client.oauth2_client.get_access_token()}",
            "Content-type": "application/json",
            **self.additional_headers,
        }

    def __get_auth_header(self):
        return {
            "Authorization": f"Bearer {self.client.oauth2_client.get_access_token()}",
            **self.additional_headers,
        }

    async def get(self, url, **kwargs):
        """GET Request to BeProduct Public API

        :url: url to call
        :returns: response body as string or throws an error

        """
        throttle = _Throttle()
        full_url = self.__append_url_parameters(
            f"{self.client.public_api_url}/{url.lstrip('/')}", kwargs
        )

        while True:
            self.logger.debug(f"GET {full_url}")
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url=full_url, headers=self.__get_headers()
                ) as response:
                    if response.status == 429:
                        self.logger.debug(f"429 {full_url}")
                        if throttle.wait_or_die():
                            continue
                        else:
                            raise BeProductException(
                                "API call failed due to throttling. "
                                "Please try again later."
                            )

                    if response.status != 200:
                        raise BeProductException(
                            "API call failed. Details: \n"
                            + f"URL: {full_url} \n"
                            + f"Status code: {response.status} \n"
                            + f"Response body: {await response.text()} \n"
                        )
                    return await response.json()

    async def delete(self, url, **kwargs):
        """DELETE Request to BeProduct Public API

        :url: url to call
        :returns: response body as string or throws an error

        """
        throttle = _Throttle()
        full_url = self.__append_url_parameters(
            f"{self.client.public_api_url}/{url.lstrip('/')}", kwargs
        )
        while True:
            self.logger.debug(f"DELETE {full_url}")
            async with aiohttp.ClientSession() as session:
                async with session.delete(
                    url=full_url, headers=self.__get_headers()
                ) as response:
                    if response.status == 429:
                        if throttle.wait_or_die():
                            continue
                        else:
                            raise BeProductException(
                                "API call failed due to throttling. "
                                "Please try again later."
                            )
                    if response.status != 200:
                        raise BeProductException(
                            "API call failed. Details: \n"
                            + f"URL: {full_url} \n"
                            + f"Status code: {response.status} \n"
                            + f"Response body: {await response.text()} \n"
                        )
                    return await response.json()

    async def post(self, url, body, **kwargs):
        """POST Request to BeProduct Public API

        :url: api url
        :body: json body
        :returns: response body as string or throws an error

        """

        throttle = _Throttle()
        full_url = self.__append_url_parameters(
            f"{self.client.public_api_url}/{url.lstrip('/')}", kwargs
        )

        while True:
            self.logger.debug(f"POST {full_url}")
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url=full_url, json=body, headers=self.__get_headers()
                ) as response:
                    if response.status == 429:
                        self.logger.debug(f"429 {full_url}")
                        if throttle.wait_or_die():
                            continue
                        else:
                            raise BeProductException(
                                "API call failed due to throttling. "
                                "Please try again later."
                            )
                    if response.status != 200:
                        raise BeProductException(
                            "API call failed. Details: \n"
                            + f"URL: {full_url} \n"
                            + f"Status code: {response.status} \n"
                            + f"Response body: {await response.text()} \n"
                        )
                    return await response.json()

    async def upload_local_file(
        self, filepath: str, url: str, body: Dict = None, **kwargs
    ):
        """Uploads a file from the filesystem using streaming
        :filepath: path of the file
        :url: api url
        :body: Dict body
        :returns: Upload ID. Check status using upload_completed
        """
        throttle = _Throttle()
        full_url = self.__append_url_parameters(
            f"{self.client.public_api_url}/{url.lstrip('/')}", kwargs
        )

        # Get file info
        try:
            file_size = os.path.getsize(filepath)
            filename = os.path.basename(filepath)
        except OSError as e:
            raise BeProductException(f"Failed to access file: {str(e)}")

        # Create multipart form data with streaming
        data = aiohttp.FormData()
        if body:
            for key, value in body.items():
                data.add_field(key, value)

        # Create a streaming reader for the file
        async def file_stream():
            with open(filepath, "rb") as f:
                while chunk := f.read(8192):  # 8KB chunks
                    yield chunk

        # Add the streaming file to form data
        data.add_field(
            "file",
            file_stream(),
            filename=filename,
            content_type="application/octet-stream",
        )

        # Upload to destination while streaming
        while True:
            self.logger.debug(f"POST {full_url}")
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url=full_url, data=data, headers=self.__get_auth_header()
                ) as response:
                    if response.status == 429:
                        self.logger.debug(f"429 {full_url}")
                        if await throttle.wait_or_die():
                            continue
                        else:
                            raise BeProductException(
                                "API call failed due to throttling. "
                                "Please try again later."
                            )
                    if response.status != 200:
                        raise BeProductException(
                            "API POST call failed. Details:\n"
                            + f"URL: {full_url} \n"
                            + f"Body: {json.dumps(body)} \n"
                            + f"Status code: {response.status} \n"
                            + f"Response body: {await response.text()} \n"
                        )
                    return await response.json()

    async def upload_from_url(
        self, file_url: str, api_url: str, body: Dict = None, **kwargs
    ):
        """Uploads a file from a URL using streaming proxy
        :file_url: url of the file to download
        :api_url: api url to upload to
        :body: Dict body
        :returns: Upload ID. Check status using upload_completed
        """
        throttle = _Throttle()
        full_url = self.__append_url_parameters(
            f"{self.client.public_api_url}/{api_url.lstrip('/')}", kwargs
        )

        # First get the file info from the source URL
        async with aiohttp.ClientSession() as session:
            async with session.head(file_url) as response:
                if response.status != 200:
                    raise BeProductException(
                        f"Failed to get file info from URL. Status: {response.status}"
                    )
                content_length = response.headers.get("content-length")
                if not content_length or not content_length.isdigit():
                    raise BeProductException(
                        "Source URL must provide a valid content-length header"
                    )
                content_type = response.headers.get(
                    "content-type", "application/octet-stream"
                )
                filename = os.path.basename(file_url).split("?")[0]

        # Create multipart form data with streaming
        data = aiohttp.FormData()
        if body:
            for key, value in body.items():
                data.add_field(key, value)

        # Stream the file directly from source to destination
        async with aiohttp.ClientSession() as session:
            # Get the file stream from source URL
            async with session.get(file_url) as source_response:
                if source_response.status != 200:
                    raise BeProductException(
                        f"Failed to download file from URL. Status: {source_response.status}"
                    )

                # Create a streaming reader for the source file
                async def file_stream():
                    async for chunk in source_response.content.iter_chunked(
                        8192
                    ):  # 8KB chunks
                        yield chunk

                # Add the streaming file to form data
                data.add_field(
                    "file", file_stream(), filename=filename, content_type=content_type
                )

                # Upload to destination while streaming
                while True:
                    self.logger.debug(f"POST {full_url}")
                    async with session.post(
                        url=full_url, data=data, headers=self.__get_auth_header()
                    ) as response:
                        if response.status == 429:
                            self.logger.debug(f"429 {full_url}")
                            if await throttle.wait_or_die():
                                continue
                            else:
                                raise BeProductException(
                                    "API call failed due to throttling. "
                                    "Please try again later."
                                )
                        if response.status != 200:
                            raise BeProductException(
                                "API POST call failed. Details:\n"
                                + f"URL: {full_url} \n"
                                + f"Body: {json.dumps(body)} \n"
                                + f"Status code: {response.status} \n"
                                + f"Response body: {await response.text()} \n"
                            )
                        return await response.json()

    async def upload_status(self, file_id: str):
        """
        Checks if file was successfully processed at BeProduct
        :returns: Tuple ( upload_is_completed, error_happened, error_msg )
        """
        self.logger.debug(f"GET {f"Style/GetImageProcessingStatus/{file_id}"}")
        status = await self.get(f"Style/GetImageProcessingStatus/{file_id}")
        self.logger.debug(f"Status: {status}")
        return status["finished"], status["errorOccured"], status["message"]
