"""
File: _color_async.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: BeProduct Public API color methods - Async Version
"""

from .sdk_async import BeProductAsync

from ._common_upload_async import UploadMixinAsync
from ._common_attributes_async import AttributesMixinAsync
from ._common_apps_async import AppsMixinAsync
from ._common_comments_async import CommentsMixinAsync
from ._common_revisions_async import RevisionsMixinAsync
from ._common_share_async import ShareMixinAsync
from ._common_tags_async import TagsMixinAsync


class ColorAsync(UploadMixinAsync, AttributesMixinAsync, AppsMixinAsync, CommentsMixinAsync,
            RevisionsMixinAsync, ShareMixinAsync, TagsMixinAsync):
    """
    Implements color API - Async Version
    """

    def __init__(self, client: BeProductAsync):
        self.client = client
        self.master_folder = 'Color'

    async def attributes_update(self, header_id: str, fields=None, colors=None):
        """Updates color attributes asynchronously

        :header_id: ID of the color
        :fields: Dictionary of fields {'field_id':'field_value'}
        :colors: List of colors in the palette/attributes
        :returns: dictionary of the requested color attributes

        """

        # transform attributes dictionary
        unwound_attributes_fields = []
        if fields:
            for field_id in fields:
                unwound_attributes_fields.append({
                    'id': field_id,
                    'value': fields[field_id]
                })

        return await self.client.raw_api.post(f"color/Header/{header_id}/Update", {
            'fields': unwound_attributes_fields,
            'colors': colors
        })

    async def attributes_create(self, folder_id: str, fields, colors=None):
        """Creates new color palette asynchronously

        :folder_id: ID of the folder to create in
        :fields: Dictionary of fields {'field_id':'field_value'}
        :returns: dictionary of the created color attributes
        :colors: List of colors in the palette/attributes 
        """

        # transform attributes dictionary
        unwound_attributes_fields = []
        for field_id in fields:
            unwound_attributes_fields.append({
                'id': field_id,
                'value': fields[field_id]
            })

        return await self.client.raw_api.post(
            f"color/Header/Create?folderId={folder_id}", {
                'fields': unwound_attributes_fields,
                'colors': colors
            }) 