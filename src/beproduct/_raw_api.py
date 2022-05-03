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
import requests
import time
import logging

from ._exception import BeProductException
from ._encoder import MultipartEncoder, FileFromURLWrapper
from .sdk import BeProduct


class _Throttle:
    """ Implements throttling policy """

    def __init__(self, strategy=None):
        """ Constrictor """
        self.strategy = strategy or [1, 3, 5, 15, 30]  # seconds to wait
        self.current = 0  # index in strategy

    def wait_or_die(self):
        """ Used to retry api calls

        :returns: True if waited, False not going to wait anymore

        """
        if len(self.strategy) <= self.current:
            return False

        logging.info(f"Throttling. Waiting {self.strategy[self.current]} sec.")
        time.sleep(self.strategy[self.current])

        self.current += 1
        return True


class RawApi:
    """Raw API class"""

    def __init__(self, client: BeProduct):
        self.client = client

    def __get_headers(self):
        return {
            'Authorization':
            f"Bearer {self.client.oauth2_client.get_access_token()}",
            'Content-type': 'application/json',
        }

    def __get_auth_header(self):
        return {
            'Authorization':
            f"Bearer {self.client.oauth2_client.get_access_token()}"
        }

    def get(self, url):
        """ GET Request to BeProduct Public API

        :url: url to call
        :returns: response body as string or throws an error

        """
        throttle = _Throttle()
        full_url = f"{self.client.public_api_url}/{url.lstrip('/')}"
        while True:
            response = requests.get(url=full_url, headers=self.__get_headers())
            if response.status_code == 429 and throttle.wait_or_die():
                continue
            break

        if response.status_code != 200:
            raise BeProductException(
                "API call failed. Details: \n" + f"URL: {full_url} \n" +
                f"Status code: {response.status_code} \n" +
                f"Response body: {response.text} \n")

        return response.json()

    def delete(self, url):
        """ DELETE Request to BeProduct Public API

        :url: url to call
        :returns: response body as string or throws an error

        """
        throttle = _Throttle()
        full_url = f"{self.client.public_api_url}/{url.lstrip('/')}"
        while True:
            response = requests.delete(url=full_url,
                                       headers=self.__get_headers())
            if response.status_code == 429 and throttle.wait_or_die():
                continue
            break

        if response.status_code != 200:
            raise BeProductException(
                "API call failed. Details: \n" + f"URL: {full_url} \n" +
                f"Status code: {response.status_code} \n" +
                f"Response body: {response.text} \n")

        return response.json()

    def post(self, url, body):
        """ POST Request to BeProduct Public API

        :url: api url
        :body: json body
        :returns: response body as string or throws an error

        """

        throttle = _Throttle()
        full_url = f"{self.client.public_api_url}/{url.lstrip('/')}"

        while True:
            response = requests.post(url=full_url,
                                     json=body,
                                     headers=self.__get_headers())
            if response.status_code == 429 and throttle.wait_or_die():
                continue
            break

        if response.status_code != 200:
            raise BeProductException(
                "API POST call failed. Details:\n" + f"URL: {full_url} \n" +
                f"Body: {json.dumps(body)} \n" +
                f"Status code: {response.status_code} \n" +
                f"Response body: {response.text} \n")

        return response.json()

    def upload_local_file(self, filepath: str, url: str, body: Dict = None):
        """ Uploads a file from the filesystem
        :filepath: path of the file
        :url: api url
        :body: Dict body
        :returns: Upload ID. Check status using upload_completed
        """

        throttle = _Throttle()
        full_url = f"{self.client.public_api_url}/{url.lstrip('/')}"

        request_body = {} if body is None else body.copy()
        f = open(filepath, 'rb')
        request_body['file'] = (os.path.basename(filepath), f,
                                'application/octet-stream')

        stream_encoder = MultipartEncoder(fields=request_body)
        headers = self.__get_auth_header()
        headers['Content-Type'] = stream_encoder.content_type

        while True:
            response = requests.post(url=full_url,
                                     data=stream_encoder,
                                     headers=headers)
            if response.status_code == 429 and throttle.wait_or_die():
                continue
            break

        f.close()

        if response.status_code != 200:
            raise BeProductException(
                "API POST call failed. Details:\n" + f"URL: {full_url} \n" +
                f"Body: {json.dumps(body)} \n" +
                f"Status code: {response.status_code} \n" +
                f"Response body: {response.text} \n")

        resp = response.json()
        return resp['imageId'] if 'imageId' in resp else None

    def upload_from_url(self, file_url: str, api_url: str, body: Dict = None):
        """ Uploads a file from the filesystem
        :file_url: url of the file
        :api_url: api url
        :body: Dict body
        :returns: Upload ID. Check status using upload_completed
        """

        throttle = _Throttle()
        full_url = f"{self.client.public_api_url}/{api_url.lstrip('/')}"

        request_body = {} if body is None else body.copy()
        request_body['file'] = (os.path.basename(file_url).split('?')[0],
                                FileFromURLWrapper(file_url),
                                'application/octet-stream')

        stream_encoder = MultipartEncoder(fields=request_body)
        headers = self.__get_auth_header()
        headers['Content-Type'] = stream_encoder.content_type

        while True:
            response = requests.post(url=full_url,
                                     data=stream_encoder,
                                     headers=headers)
            if response.status_code == 429 and throttle.wait_or_die():
                continue
            break

        if response.status_code != 200:
            raise BeProductException(
                "API POST call failed. Details:\n" + f"URL: {full_url} \n" +
                f"Body: {json.dumps(body)} \n" +
                f"Status code: {response.status_code} \n" +
                f"Response body: {response.text} \n")

        resp = response.json()
        return resp['imageId'] if 'imageId' in resp else None

    def upload_status(self, file_id: str):
        """
        Checks if file was successfully processed at BeProduct
        :returns: Tuple ( upload_is_completed, error_happened, error_msg )
        """
        status = self.get(f"Style/GetImageProcessingStatus/{file_id}")

        return status["finished"], status["errorOccured"], status["message"]
