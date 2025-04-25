"""
File: _directory_async.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: Async implementation of BeProduct Directory API
"""
from .sdk_async import BeProductAsync
from typing import Dict, Any, Optional, List


class DirectoryAsync:

    """ Implements Directory API - Async Version """

    def __init__(self, client: BeProductAsync):
        """ Constructor """
        self.client = client

    async def directory_list(self, page_size: int = 20):
        """Get list of directory records asynchronously
        :page_size: Page size. Determines how many calls to api you
                    need to make to get whole directory list
        :returns: Async iterator of directory records

        """
        async def async_iterator():
            page_number = 0
            while True:
                page = await self.client.raw_api.get(
                        f"Directory/Companies?pageNumber={page_number}&pageSize={page_size}")
                if not page:
                    break
                for dir in page:
                    yield dir
                page_number += 1

        return async_iterator()

    async def directory_get(self, header_id: str):
        """Gets a directory partner/factory/vendor by ID asynchronously

        :header_id: Id of the directory record
        :returns: Directory record

        """
        return await self.client.raw_api.get(
                f"Directory/Company?directoryId={header_id}")

    async def directory_contact_list(self, header_id: str, page_size: int = 20):
        """Gets list of contacts for a given directory record asynchronously

        :header_id: Id of the directory record
        :page_size: Page size. Determines how many calls to api you
                    need to make to get whole contact list
        :returns: Async iterator of contacts for the given directory record

        """
        async def async_iterator():
            page_number = 0
            while True:
                page = await self.client.raw_api.get(
                        f"Directory/Contacts?directoryId={header_id}&" +
                        f"pageNumber={page_number}&pageSize={page_size}")
                if not page:
                    break
                for dir in page:
                    yield dir
                page_number += 1

        return async_iterator()

    async def directory_contact_get(self, header_id: str, contact_id: str):
        """Returns a single contact from provided directory record asynchronously

        :header_id: Id of the directory record
        :contact_id: Contact ID
        :returns: Contact dictionary

        """
        return await self.client.raw_api.get(
                f"Directory/Contact?directoryId={header_id}" +
                f"&contactId={contact_id}")

    async def directory_add(self, fields):
        """Adds new directory record asynchronously

        :fields: Directory record dictionary
        :returns: Created directory record dictionary

        """
        return await self.client.raw_api.post('Directory/Add', body=fields)

    async def directory_contact_add(self, header_id: str, fields):
        """Adds new contact to existing directory record asynchronously

        :fields: Contact dictionary
        :returns: Created contact dictionary

        """
        return await self.client.raw_api.post(
                f"Directory/{header_id}/Contact/Add",
                body=fields) 