"""
File: _directory.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: Directory Public API
"""

from .sdk import BeProduct, BeProductAsync


class Directory:
    """Implements Directory API"""

    def __init__(self, client: BeProduct | BeProductAsync):
        """Constructor"""
        self.client = client
        if isinstance(self.client, BeProductAsync):
            self.directory_list = self._directory_list_async
            self.directory_contact_list = self._directory_contact_list_async
            self.directory_search = self._directory_search_async

    def directory_list(self, page_size: int = 20):
        """Get list of directory records
        :page_size: Page size. Determines how many calls to api you
                    need to make to get whole directory list
        :returns: List of directory records

        """
        page_number = 0

        while True:
            page = self.client.raw_api.get(
                f"Directory/Companies?pageNumber={page_number}&pageSize={page_size}"
            )
            if not page:
                break
            for dir in page:
                yield dir
            page_number += 1

    async def _directory_list_async(self, page_size: int = 20):
        """Get list of directory records
        :page_size: Page size. Determines how many calls to api you
                    need to make to get whole directory list
        :returns: List of directory records

        """
        page_number = 0

        while True:
            page = await self.client.raw_api.get(
                f"Directory/Companies?pageNumber={page_number}&pageSize={page_size}"
            )
            if not page:
                break
            for dir in page:
                yield dir
            page_number += 1

    def directory_get(self, header_id: str):
        """Gets a directory partner/factory/vendor by ID

        :header_id: Id of the directory record
        :returns: Directory record

        """

        return self.client.raw_api.get(f"Directory/Company?directoryId={header_id}")

    def directory_contact_list(self, header_id: str, page_size: int = 20):
        """Gets list of contacts for a given directory record

        :header_id: Id of the directory record
        :page_size: Page size. Determines how many calls to api you
                    need to make to get whole contact list
        :returns: List of contacts for the given directory record

        """
        page_number = 0

        while True:
            page = self.client.raw_api.get(
                f"Directory/Contacts?directoryId={header_id}&"
                + f"pageNumber={page_number}&pageSize={page_size}"
            )
            if not page:
                break
            for dir in page:
                yield dir
            page_number += 1

    async def _directory_contact_list_async(self, header_id: str, page_size: int = 20):
        """Gets list of contacts for a given directory record
        :header_id: Id of the directory record
        :page_size: Page size. Determines how many calls to api you
                    need to make to get whole contact list
        :returns: List of contacts for the given directory record
        """
        page_number = 0
        while True:
            page = await self.client.raw_api.get(
                f"Directory/Contacts?directoryId={header_id}&"
                + f"pageNumber={page_number}&pageSize={page_size}"
            )
            if not page:
                break
            for dir in page:
                yield dir
            page_number += 1

    def directory_contact_get(self, header_id: str, contact_id: str):
        """Returns a single contact from provided directory record

        :header_id: Id of the directory record
        :contact_id: Contact ID
        :returns: Contact dictionary

        """
        return self.client.raw_api.get(
            f"Directory/Contact?directoryId={header_id}" + f"&contactId={contact_id}"
        )

    def directory_add(self, fields):
        """Adds new directory record

        :fields: Directory record dictionary
        :returns: Created directory record dictionary

        """
        return self.client.raw_api.post("Directory/Add", body=fields)

    def directory_contact_add(self, header_id: str, fields):
        """Adds new contact to existing directory record

        :fields: Contact dictionary
        :returns: Created contact dictionary

        """
        return self.client.raw_api.post(
            f"Directory/{header_id}/Contact/Add", body=fields
        )

    def directory_update(self, header_id: str, fields):
        """Updates a directory record

        :header_id: Id of the directory record
        :fields: Directory record dictionary

        """
        return self.client.raw_api.post(f"Directory/Update/{header_id}", body=fields)

    def directory_contact_update(self, header_id: str, contact_id: str, fields):
        """Updates a contact of a directory record

        :header_id: Id of the directory record
        :contact_id: Contact ID
        :fields: Contact dictionary

        """
        return self.client.raw_api.post(
            f"Directory/{header_id}/Contact/{contact_id}/Update", body=fields
        )

    def directory_search(self, filters=None, page_size: int = 20):
        """Searches directory records

        :filters: List of filter dictionaries
        :page_size: Page size
        :returns: Enumerator of directory records

        """
        page_number = 0
        while True:
            page = self.client.raw_api.post(
                f"Directory/Companies?pageNumber={page_number}&pageSize={page_size}",
                body={"filters": filters or []},
            )
            if not page:
                break
            for dir in page:
                yield dir
            page_number += 1

    async def _directory_search_async(self, filters=None, page_size: int = 20):
        """Searches directory records
        :filters: List of filter dictionaries
        :page_size: Page size
        :returns: Enumerator of directory records
        """
        page_number = 0
        while True:
            page = await self.client.raw_api.post(
                f"Directory/Companies?pageNumber={page_number}&pageSize={page_size}",
                body={"filters": filters or []},
            )
            if not page:
                break
            for dir in page:
                yield dir
            page_number += 1

