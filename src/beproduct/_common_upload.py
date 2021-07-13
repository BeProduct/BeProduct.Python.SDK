"""
File: _common_upload.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: Common Upload Mixin
"""

from ._exception import BeProductException


class UploadMixin:
    """
    Common upload methods for any master folder (Style, Material, etc.)
    """

    def __init__(self, master_folder):
        self.master_folder = master_folder

    def attributes_upload(self,
                          header_id: str,
                          filepath: str = None,
                          file_url: str = None):
        """ Uploads file to Attributes
        :id: ID of the Style, Material etc
        :filepath: Local file path
        :file_url: Remote file URL
        :returns File ID
        """
        if filepath:
            return self.client.raw_api.upload_local_file(
                filepath,
                f"{self.master_folder}/Header/{header_id}/Image/Upload"
            )
        if file_url:
            return self.client.raw_api.upload_from_url(
                file_url,
                f"{self.master_folder}/Header/{header_id}/Image/Upload",
            )
        return BeProductException("No file provided")

    def upload_status(self, upload_id: str):
        """ Checks upload status
        :returns: Tuple (is_finished, is_error, error_msg)
        """
        return self.client.raw_api.upload_status(upload_id)
