"""
File: _image.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: BeProduct Public API Block methods
"""

from .sdk import BeProduct

from ._common_upload import UploadMixin
from ._common_attributes import AttributesMixin
from ._common_apps import AppsMixin
from ._common_comments import CommentsMixin
from ._common_revisions import RevisionsMixin
from ._common_share import ShareMixin
from ._common_tags import TagsMixin

from ._exception import BeProductException


class Block(
        UploadMixin,
        AttributesMixin,
        AppsMixin,
        CommentsMixin,
        RevisionsMixin,
        ShareMixin,
        TagsMixin):

    """
    Implements Block API
    """

    def __init__(self, client: BeProduct):
        self.client = client
        self.master_folder = 'Block'

    def attributes_update(
            self,
            header_id: str,
            fields=None,
            size_classes=None):
        """Updates Block attributes

        :header_id: ID of the Block
        :fields: Dictionary of fields {'field_id':'field_value'}
        :size_classes: Size Classes dictionary
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
            f"Block/Header/{header_id}/Update",
            {
                'fields': unwound_attributes_fields,
                'sizeClasses': size_classes
            })

    def attributes_create(
            self,
            folder_id: str,
            fields,
            size_classes=None):
        """Creates new Block

        :folder_id: ID of the folder to create in
        :fields: Dictionary of fields {'field_id':'field_value'}
        :size_classes: Size Classes dictionary
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
            f"Block/Header/Create?folderId={folder_id}",
            {
                'fields': unwound_attributes_fields,
                'sizeClasses': size_classes
            })

    def app_block_size_class_3d_asset_upload(
            self,
            header_id: str,
            size_class_id_or_name: str,
            filepath: str = None,
            fileurl: str = None):
        """ Uploads a 3D file into Block Size Class

        :header_id: Header ID,
        :size_class_id_or_name: Size Class ID
        :filepath: Local file path
        :fileurl: Remote file URL
        :returns: Upload ID

        """

        if filepath:
            return self.client.raw_api.upload_local_file(
                filepath,
                f"Block/SizeClass3DAssetUpload?headerId={header_id}" +
                f"&sizeClass={size_class_id_or_name}")
        if fileurl:
            return self.client.raw_api.upload_from_url(
                fileurl,
                f"Block/SizeClass3DAssetUpload?headerId={header_id}" +
                f"&sizeClass={size_class_id_or_name}")

        return BeProductException("No file provided")
