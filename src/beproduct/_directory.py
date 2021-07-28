"""
File: _directory.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: Directory Public API
"""
from .sdk import BeProduct


class Directory:

    """ Implements Directory API """

    def __init__(self, client: BeProduct):
        """ Constructor """
        self.client = client

    def directory_list(self, page_size: int = 20):
        """Get list of directory records
        :page_size: Page size. Determines how many calls to api you
                    need to make to get whole directory list
        :returns: List of directory records

        """
        page_number = 0

        while True:
            page = self.client.raw_api.get(
                    f"Directory/Companies?pageNumber={page_number}&pageSize={page_size}")
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

        return self.client.raw_api.get(
                f"Directory/Company?directoryId={header_id}")

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
                    f"Directory/Contacts?directoryId={header_id}&" +
                    f"pageNumber={page_number}&pageSize={page_size}")
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
                f"Directory/Contact?directoryId={header_id}" +
                f"&contactId={contact_id}")

    def directory_add(self, fields):
        """Adds new directory record

        :fields: Directory record dictionary
        :returns: Created directory record dictionary

        """
        return self.client.raw_api.post('Directory/Add', body=fields)

    def directory_contact_add(self, header_id: str, fields):
        """Adds new contact to existing directory record

        :fields: Contact dictionary
        :returns: Created contact dictionary

        """
        return self.client.raw_api.post(
                f"Directory/{header_id}/Contact/Add",
                body=fields)
