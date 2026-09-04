"""
File: _inbox.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: Inbox (tasks and messages) Public API
"""

from .sdk import BeProduct, BeProductAsync


class Inbox:
    """Implements Inbox API — tasks and their messages"""

    def __init__(self, client: BeProduct | BeProductAsync):
        """Constructor"""
        self.client = client

    def task_list(self, master_folder: str, filters=None, folder_id: str = None, page_size: int = 30):
        """Lists inbox tasks for a master folder, optionally filtered

        :master_folder: 'Style', 'Material', 'Image' or 'Color'
        :filters: List of filter dictionaries
        :folder_id: Restrict to one folder (optional)
        :page_size: Page size
        :returns: Enumerator of tasks

        """
        folder = f"&folderId={folder_id}" if folder_id else ""
        return self.client.beproduct_paging_iterator(
            page_size,
            lambda psize, pnum: self.client.raw_api.post(
                f"Inbox/Tasks/{master_folder}?pageSize={psize}&pageNumber={pnum}{folder}",
                body={"filters": filters or []},
            ),
        )

    def task_get(self, task_id: str):
        """Gets one task

        :task_id: Task ID
        :returns: Task dictionary

        """
        return self.client.raw_api.get(f"Inbox/Task/{task_id}")

    def task_create(self, fields):
        """Creates a task

        :fields: Task dictionary
        :returns: Created task

        """
        return self.client.raw_api.post("Inbox/Task/Create", body=fields)

    def task_update(self, task_id: str, fields):
        """Updates a task

        :task_id: Task ID
        :fields: Task dictionary

        """
        return self.client.raw_api.post(f"Inbox/Task/{task_id}/Update", body=fields)

    def task_delete(self, task_id: str):
        """Deletes a task

        :task_id: Task ID

        """
        return self.client.raw_api.delete(f"Inbox/Task/{task_id}/Delete")

    def message_list(self, task_id: str, page_size: int = 30):
        """Lists the messages of a task

        :task_id: Task ID
        :page_size: Page size
        :returns: Enumerator of messages

        """
        return self.client.beproduct_paging_iterator(
            page_size,
            lambda psize, pnum: self.client.raw_api.post(
                f"Inbox/Task/{task_id}/Messages?pageSize={psize}&pageNumber={pnum}", body={}
            ),
        )

    def message_create(self, task_id: str, fields):
        """Adds a message to a task

        :task_id: Task ID
        :fields: Message dictionary
        :returns: Created message

        """
        return self.client.raw_api.post(f"Inbox/Task/{task_id}/Message/Create", body=fields)

    def message_update(self, message_id: str, fields):
        """Updates a message

        :message_id: Message ID
        :fields: Message dictionary

        """
        return self.client.raw_api.post(f"Inbox/Task/Message/{message_id}/Update", body=fields)

    def message_delete(self, message_id: str):
        """Deletes a message

        :message_id: Message ID

        """
        return self.client.raw_api.delete(f"Inbox/Task/Message/{message_id}/Delete")

    def message_attachments_upload(self, message_id: str, filepath: str = None, fileurl: str = None):
        """Attaches a file to a message

        :message_id: Message ID
        :filepath: Local file path
        :fileurl: Remote file URL
        :returns: Upload ID

        """
        url = f"Inbox/Task/Message/{message_id}/AttachmentsUpload"
        if filepath:
            return self.client.raw_api.upload_local_file(filepath, url)
        if fileurl:
            return self.client.raw_api.upload_from_url(fileurl, url)
        raise ValueError("No file provided")
