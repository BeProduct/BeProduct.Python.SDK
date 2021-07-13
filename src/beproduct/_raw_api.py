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
from requests import api

from ._exception import BeProductException
from ._encoder import MultipartEncoder, FileFromURLWrapper
from .sdk import BeProduct


class RawApi:
    """Raw API class"""

    def __init__(self, client: BeProduct):
        self.client = client

    def __get_headers(self):
        return {
            'Authorization': f"Bearer {self.client.oauth2_client.get_access_token()}",
            'Content-type': 'application/json',
        }

    def __get_auth_header(self):
        return {
            'Authorization': f"Bearer {self.client.oauth2_client.get_access_token()}"
        }

    def get(self, url):
        """ Get Request to BeProduct Public API

        :url: url to call
        :returns: response body as string or throws an error

        """
        full_url = f"{self.client.public_api_url}/{url.lstrip('/')}"
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

        :url: api url
        :body: json body
        :file: optional file if file upload required
        :returns: response body as string or throws an error

        """

        full_url = f"{self.client.public_api_url}/{url.lstrip('/')}"
        response = requests.post(
            url=full_url,
            json=body,
            headers=self.__get_headers())

        if response.status_code != 200:
            raise BeProductException(
                "API POST call failed. Details:\n" +
                f"URL: {full_url} \n" +
                f"Body: {json.dumps(body)} \n" +
                f"Status code: {response.status_code} \n" +
                f"Response body: {response.text} \n")

        return response.json()

    def upload_local_file(self, filepath: str, url: str, body: Dict = None):
        """ Uploads a file from the filesystem
        :filepath: path of the file
        :url: api url
        :body: Dict body
        :returns: File ID. Check status using upload_completed
        """

        full_url = f"{self.client.public_api_url}/{url.lstrip('/')}"

        request_body = {} if body is None else body.copy()
        request_body['file'] = (
            os.path.basename(filepath),
            open(filepath, 'rb'),
            'application/octet-stream')

        stream_encoder = MultipartEncoder(fields=request_body)
        headers = self.__get_auth_header()
        headers['Content-Type'] = stream_encoder.content_type

        response = requests.post(
            url=full_url,
            data=stream_encoder,
            headers=headers)

        if response.status_code != 200:
            raise BeProductException(
                "API POST call failed. Details:\n" +
                f"URL: {full_url} \n" +
                f"Body: {json.dumps(body)} \n" +
                f"Status code: {response.status_code} \n" +
                f"Response body: {response.text} \n")

        return response.json()["imageId"]

    def upload_from_url(self, file_url: str, api_url: str, body: Dict = None):
        """ Uploads a file from the filesystem
        :file_url: url of the file
        :api_url: api url
        :body: Dict body
        :returns: File ID. Check status using upload_completed
        """

        full_url = f"{self.client.public_api_url}/{api_url.lstrip('/')}"

        request_body = {} if body is None else body.copy()
        request_body['file'] = (
            os.path.basename(file_url),
            FileFromURLWrapper(file_url),
            'application/octet-stream')

        stream_encoder = MultipartEncoder(fields=request_body)
        headers = self.__get_auth_header()
        headers['Content-Type'] = stream_encoder.content_type

        response = requests.post(
            url=full_url,
            data=stream_encoder,
            headers=headers)

        if response.status_code != 200:
            raise BeProductException(
                "API POST call failed. Details:\n" +
                f"URL: {full_url} \n" +
                f"Body: {json.dumps(body)} \n" +
                f"Status code: {response.status_code} \n" +
                f"Response body: {response.text} \n")

        return response.json()["imageId"]

    def upload_status(self, file_id: str):
        """
        Checks if file was successfully processed at BeProduct
        :returns: Tuple ( upload_is_completed, error_happened, error_msg )
        """
        status = self.get(f"Style/GetImageProcessingStatus/{file_id}")

        return status["finished"], status["errorOccured"], status["message"] 
