"""
File: _block_async.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: BeProduct Public API Block methods - Async Version
"""

from .sdk_async import BeProductAsync

from ._common_upload_async import UploadMixinAsync
from ._common_attributes_async import AttributesMixinAsync
from ._common_apps_async import AppsMixinAsync
from ._common_comments_async import CommentsMixinAsync
from ._common_revisions_async import RevisionsMixinAsync
from ._common_share_async import ShareMixinAsync
from ._common_tags_async import TagsMixinAsync

from ._exception import BeProductException


class BlockAsync(
        UploadMixinAsync,
        AttributesMixinAsync,
        AppsMixinAsync,
        CommentsMixinAsync,
        RevisionsMixinAsync,
        ShareMixinAsync,
        TagsMixinAsync):

    """
    Implements Block API - Async Version
    """

    def __init__(self, client: BeProductAsync):
        self.client = client
        self.master_folder = 'Block'

    async def attributes_update(
            self,
            header_id: str,
            fields=None,
            size_classes=None):
        """Updates Block attributes asynchronously

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

        return await self.client.raw_api.post(
            f"Block/Header/{header_id}/Update",
            {
                'fields': unwound_attributes_fields,
                'sizeClasses': size_classes
            })

    async def attributes_create(
            self,
            folder_id: str,
            fields,
            size_classes=None):
        """Creates new Block asynchronously

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

        return await self.client.raw_api.post(
            f"Block/Header/Create?folderId={folder_id}",
            {
                'fields': unwound_attributes_fields,
                'sizeClasses': size_classes
            })

    async def app_block_size_class_3d_asset_upload(
            self,
            header_id: str,
            size_class_id_or_name: str,
            filepath: str = None,
            fileurl: str = None):
        """ Uploads a 3D file into Block Size Class asynchronously

        :header_id: Header ID,
        :size_class_id_or_name: Size Class ID
        :filepath: Local file path
        :fileurl: Remote file URL
        :returns: Upload ID

        """

        if filepath:
            return await self.client.raw_api.upload_local_file(
                filepath,
                f"Block/SizeClass3DAssetUpload?headerId={header_id}" +
                f"&sizeClass={size_class_id_or_name}")
        if fileurl:
            return await self.client.raw_api.upload_from_url(
                fileurl,
                f"Block/SizeClass3DAssetUpload?headerId={header_id}" +
                f"&sizeClass={size_class_id_or_name}")

        return BeProductException("No file provided") 