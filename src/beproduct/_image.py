"""
File: _image.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: BeProduct Public API Image methods
"""

from .sdk import BeProduct

from ._common_upload import UploadMixin
from ._common_attributes import AttributesMixin
from ._common_apps import AppsMixin
from ._common_comments import CommentsMixin
from ._common_revisions import RevisionsMixin
from ._common_share import ShareMixin
from ._common_tags import TagsMixin


class Image(
        UploadMixin,
        AttributesMixin,
        AppsMixin,
        CommentsMixin,
        RevisionsMixin,
        ShareMixin,
        TagsMixin):

    """
    Implements Image API
    """

    def __init__(self, client: BeProduct):
        self.client = client
        self.master_folder = 'Image'

    def attributes_update(self, header_id: str, fields=None):
        """Updates image attributes

        :header_id: ID of the image
        :fields: Dictionary of fields {'field_id':'field_value'}
        :returns: dictionary of the requested image attributes

        """

        # transform attributes dictionary
        unwound_attributes_fields = []
        if fields:
            for field_id in fields:
                unwound_attributes_fields.append({
                    'id': field_id,
                    'value': fields[field_id]
                })

        return self.client.raw_api.post(
            f"Image/Header/{header_id}/Update",
            {
                'fields': unwound_attributes_fields
            })

    def attributes_create(
            self,
            folder_id: str,
            fields,
            force_version_update: bool = False):
        """Creates new image

        :folder_id: ID of the folder to create in
        :fields: Dictionary of fields {'field_id':'field_value'}
        :force_version_update: If true, the header version from fields will be applied on creation
        :returns: dictionary of the created image attributes
        """

        # transform attributes dictionary
        unwound_attributes_fields = []
        for field_id in fields:
            unwound_attributes_fields.append({
                'id': field_id,
                'value': fields[field_id]
            })

        return self.client.raw_api.post(
            f"Image/Header/Create?folderId={folder_id}&preserveVersion={str(force_version_update).lower()}",
            {
                'fields': unwound_attributes_fields
            })

    def attributes_image_version_upload(self, header_id: str, filepath: str = None, fileurl: str = None):
        """Uploads a new version of the image header's main image

        :header_id: Image ID
        :filepath: Local file path
        :fileurl: Remote file URL
        :returns: Upload ID

        """
        url = f"Image/Header/{header_id}/Image/Upload"
        if filepath:
            return self.client.raw_api.upload_local_file(filepath, url)
        if fileurl:
            return self.client.raw_api.upload_from_url(fileurl, url)
        raise ValueError("No file provided")

