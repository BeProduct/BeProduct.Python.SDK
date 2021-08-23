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
                          fileurl: str = None,
                          position: str = None):
        """ Uploads file to Attributes
        :header_id: ID of the Style, Material etc
        :filepath: Local file path
        :fileurl: Remote file URL
        :position: Position to upload. Leave empty for default upload
                   For style 'front','side' or 'back'.
                   For material: 'main' or 'detail'
        :returns: Upload ID
        """
        if filepath:
            return self.client.raw_api.upload_local_file(
                filepath,
                f"{self.master_folder}/Header/{header_id}/Image/Upload" +
                (f"/Position/{position}" if position else '')
            )
        if fileurl:
            return self.client.raw_api.upload_from_url(
                fileurl,
                f"{self.master_folder}/Header/{header_id}/Image/Upload" +
                (f"/Position/{position}" if position else '')
            )
        return BeProductException("No file provided")

    def app_list_upload(self,
                        header_id: str,
                        app_id: str,
                        list_item_id: str,
                        filepath: str = None,
                        fileurl: str = None):
        """ Uploads image to List/List-Form/List-Grid apps

        :header_id: ID of the Style, Material etc
        :app_id: Application ID
        :list_item_id: Id of the List item
        :filepath: Local file path
        :fileurl: Remote file URL
        :returns: Upload ID
        """

        if filepath:
            return self.client.raw_api.upload_local_file(
                filepath,
                f"{self.master_folder}/ListAppImageUpload?" +
                f"{self.master_folder.lower()}Id={header_id}" +
                f"&pageId={app_id}&listItemId={list_item_id}"
            )
        if fileurl:
            return self.client.raw_api.upload_from_url(
                fileurl,
                f"{self.master_folder}/ListAppImageUpload?" +
                f"{self.master_folder.lower()}Id={header_id}" +
                f"&pageId={app_id}&listItemId={list_item_id}"
            )
        return BeProductException("No file provided")

    def app_attachments_upload(
            self,
            header_id: str,
            app_id: str,
            filepath: str = None,
            fileurl: str = None):
        """ Uploads image to Attachment app
        :header_id: ID of the Style, Material etc
        :app_id: Application ID
        :filepath: Local file path
        :fileurl: Remote file URL
        :returns: Upload ID
        """

        if filepath:
            return self.client.raw_api.upload_local_file(
                filepath,
                f"{self.master_folder}/AttachmentUpload?" +
                f"{self.master_folder.lower()}Id={header_id}" +
                f"&pageId={app_id}"
            )
        if fileurl:
            return self.client.raw_api.upload_from_url(
                fileurl,
                f"{self.master_folder}/AttachmentUpload?" +
                f"{self.master_folder.lower()}Id={header_id}" +
                f"&pageId={app_id}"
            )
        return BeProductException("No file provided")

    def app_imageform_upload(
            self,
            header_id: str,
            app_id: str,
            filepath: str = None,
            fileurl: str = None):
        """Uploads image in ImageForm application

        :header_id: ID of the Style, Material etc
        :app_id: Application ID
        :filepath: Local file path
        :fileurl: Remote file URL
        :returns: Upload ID

        """
        if filepath:
            return self.client.raw_api.upload_local_file(
                filepath,
                f"{self.master_folder}/GridFormImageAppImageUpload?" +
                f"{self.master_folder.lower()}Id={header_id}" +
                f"&pageId={app_id}"
            )
        if fileurl:
            return self.client.raw_api.upload_from_url(
                fileurl,
                f"{self.master_folder}/GridFormImageAppImageUpload?" +
                f"{self.master_folder.lower()}Id={header_id}" +
                f"&pageId={app_id}"
            )
        return BeProductException("No file provided")

    def app_imagegrid_upload(
            self,
            header_id: str,
            app_id: str,
            filepath: str = None,
            fileurl: str = None):
        """Uploads image in ImageGrid application

        :header_id: ID of the Style, Material etc
        :app_id: Application ID
        :filepath: Local file path
        :fileurl: Remote file URL
        :returns: Upload ID

        """
        return self.app_imageform_upload(
            header_id=header_id,
            app_id=app_id,
            filepath=filepath,
            fileurl=fileurl)

    def upload_status(self, upload_id: str):
        """ Checks upload status

        :returns: Tuple (is_finished, is_error, error_msg)
        """
        return self.client.raw_api.upload_status(upload_id)
