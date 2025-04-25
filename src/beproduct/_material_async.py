"""
File: _material_async.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: BeProduct Public API material methods - Async Version
"""

from typing import Dict, Any, Optional, List, Union
from ._common_upload_async import UploadMixinAsync
from ._common_attributes_async import AttributesMixinAsync
from ._common_apps_async import AppsMixinAsync
from ._common_comments_async import CommentsMixinAsync
from ._common_revisions_async import RevisionsMixinAsync
from ._common_share_async import ShareMixinAsync
from ._common_tags_async import TagsMixinAsync
from ._exception import BeProductException
from .sdk_async import BeProductAsync

class MaterialAsync(
    UploadMixinAsync,
    AttributesMixinAsync,
    AppsMixinAsync,
    CommentsMixinAsync,
    RevisionsMixinAsync,
    ShareMixinAsync,
    TagsMixinAsync,
):
    """
    Implements Material API - Async Version
    """

    def __init__(self, client: BeProductAsync):
        """Constructor
        :param client: AsyncBeProduct instance
        """
        self.client = client
        self.master_folder = 'Material'

    async def attributes_update(self,
                          header_id: str,
                          fields=None,
                          colorways=None,
                          sizes=None,
                          suppliers=None):
        """Updates material attributes asynchronously

        :header_id: ID of the material
        :fields: Dictionary of fields {'field_id':'field_value'}
        :colorways: Dictionary in Colorway update format
        :sizes: Dictionary in Size format
        :suppliers: List of supplier dictionaries
        :returns: dictionary of the requested material attributes

        """

        # transform attributes dictionary
        unwound_attributes_fields = []
        if fields:
            for field_id in fields:
                unwound_attributes_fields.append({
                    'id': field_id,
                    'value': fields[field_id]
                })

        # transform colorway dictionary
        colorway_fields = []
        if colorways:
            for color in colorways:
                unwound_colorway_fields = []

                for field_id in color['fields']:
                    unwound_colorway_fields.append({
                        'id': field_id,
                        'value': color['fields'][field_id]
                    })

                colorway_fields.append({
                    'id': color['id'],
                    'fields': unwound_colorway_fields
                })

        return await self.client.raw_api.post(
            f"Material/Header/{header_id}/Update", {
                'fields': unwound_attributes_fields,
                'colorways': colorway_fields,
                'sizes': sizes,
                'suppliers': suppliers
            })

    async def attributes_create(self,
                          folder_id: str,
                          fields,
                          colorways=None,
                          sizes=None,
                          suppliers=None):
        """Creates new material asynchronously

        :folder_id: ID of the folder to create in
        :fields: Dictionary of fields {'field_id':'field_value'}
        :colorways Dictionary of colorway fields
        :sizes Dictionary in Size format
        :suppliers: List of supplier dictionaries
        :returns: dictionary of the created material attributes
        """

        # transform attributes dictionary
        unwound_attributes_fields = []
        for field_id in fields:
            unwound_attributes_fields.append({
                'id': field_id,
                'value': fields[field_id]
            })

        # transform colorway dictionary
        colorway_fields = []
        if colorways:
            for color in colorways:
                unwound_colorway_fields = []

                for field_id in color['fields']:
                    unwound_colorway_fields.append({
                        'id': field_id,
                        'value': color['fields'][field_id]
                    })

                colorway_fields.append({
                    'id': color['id'],
                    'fields': unwound_colorway_fields
                })

        return await self.client.raw_api.post(
            f"Material/Header/Create?folderId={folder_id}", {
                'fields': unwound_attributes_fields,
                'colorways': colorway_fields,
                'sizes': sizes,
                'suppliers': suppliers
            })

    async def attributes_colorway_delete(self, header_id: str, colorway_id: str):
        """Deletes single colorway from Attributes app asynchronously

        :header_id: Material ID
        :colorway_id: ID of the colorway to be deleted
        :returns: None

        """
        return await self.client.raw_api.get(
            f"Material/Header/{header_id}/Colorway/Delete/{colorway_id}")

    async def attributes_colorway_upload(self,
                                   header_id: str,
                                   colorway_id: str = None,
                                   filepath: str = None,
                                   fileurl: str = None,
                                   color_number: str = None):
        """Uploads colorway image asynchronously
        :header_id: Material ID
        :colorway_id: Colorway ID
        :color_number: Color number
        :filepath: Local file path
        :fileurl: Remote file URL
        :returns: Upload ID

        """
        if filepath:
            return await self.client.raw_api.upload_local_file(
                filepath,
                f"Material/Header/{header_id}/ColorwayImage/Upload?" +
                f"colorNumber={color_number}&colorId={colorway_id}")
        if fileurl:
            return await self.client.raw_api.upload_from_url(
                fileurl, f"Material/Header/{header_id}/ColorwayImage/Upload?" +
                f"colorNumber={color_number}&colorId={colorway_id}")

        return BeProductException("No file provided")

    async def app_artboard_version_upload(self,
                                    header_id: str,
                                    filepath: str = None,
                                    fileurl: str = None):
        """Uploads an image as a new version into Artboard application asynchronously

        :header_id: Material ID
        :filepath: Local file path
        :fileurl: Remote file URL
        :returns: Upload ID

        """
        if filepath:
            return await self.client.raw_api.upload_local_file(
                filepath, f"Material/Header/{header_id}/Image/Upload")
        if fileurl:
            return await self.client.raw_api.upload_from_url(
                fileurl, f"Material/Header/{header_id}/Image/Upload")

        return BeProductException("No file provided")

    async def app_3d_material_upload(self, *params):
        """
        DEPRECATED! WILL BE REMOVED IN FUTURE VERSION!
        USE app_3d_material_asset_upload """

        return await self.app_3d_material_asset_upload(*params)

    async def app_3d_material_asset_upload(self,
                                     header_id: str,
                                     app_id: str,
                                     colorway_id: str,
                                     filepath: str = None,
                                     fileurl: str = None):
        """Uploads 3D material asset asynchronously

        :header_id: Material ID
        :app_id: Application ID
        :colorway_id: Colorway ID
        :filepath: Local file path
        :fileurl: Remote file URL
        :returns: Upload ID

        """
        if filepath:
            return await self.client.raw_api.upload_local_file(
                filepath,
                f"Material/3DMaterialAssetUpload?headerId={header_id}" +
                f"&pageId={app_id}&colorwayId={colorway_id}")
        if fileurl:
            return await self.client.raw_api.upload_from_url(
                fileurl,
                f"Material/3DMaterialAssetUpload?headerId={header_id}" +
                f"&pageId={app_id}&colorwayId={colorway_id}")

        return BeProductException("No file provided")

    async def app_3d_material_preview_upload(self,
                                       header_id: str,
                                       app_id: str,
                                       colorway_id: str,
                                       filepath: str = None,
                                       fileurl: str = None):
        """Uploads 3D material preview asynchronously

        :header_id: Material ID
        :app_id: Application ID
        :colorway_id: Colorway ID
        :filepath: Local file path
        :fileurl: Remote file URL
        :returns: Upload ID

        """
        if filepath:
            return await self.client.raw_api.upload_local_file(
                filepath,
                f"Material/Material3DPreviewUpload?materialId={header_id}" +
                f"&pageId={app_id}&colorwayId={colorway_id}")
        if fileurl:
            return await self.client.raw_api.upload_from_url(
                fileurl,
                f"Material/Material3DPreviewUpload?materialId={header_id}" +
                f"&pageId={app_id}&colorwayId={colorway_id}")

        return BeProductException("No file provided")

    async def app_3d_material_texture_upload(self,
                                       header_id: str,
                                       app_id: str,
                                       colorway_id: str,
                                       side: str = 'front',
                                       filepath: str = None,
                                       fileurl: str = None):
        """Uploads 3D material texture asynchronously

        :header_id: Material ID
        :app_id: Application ID
        :colorway_id: Colorway ID
        :side: Side of the texture ('front' or 'back')
        :filepath: Local file path
        :fileurl: Remote file URL
        :returns: Upload ID

        """
        if filepath:
            return await self.client.raw_api.upload_local_file(
                filepath,
                f"Material/Material3D{side}TextureUpload?materialId={header_id}"
                + f"&pageId={app_id}&colorwayId={colorway_id}")
        if fileurl:
            return await self.client.raw_api.upload_from_url(
                fileurl,
                f"Material/Material3D{side}TextureUpload?materialId={header_id}"
                + f"&pageId={app_id}&colorwayId={colorway_id}")

        return BeProductException("No file provided")

    async def app_request_list(self, header_id: str):
        """Returns list of material requests asynchronously

        :header_id: Material ID
        :returns: List of material requests

        """
        return await self.client.raw_api.get(
            f"Material/RequestPages?headerId={header_id}")

    async def app_request_get(self,
                        header_id: str,
                        app_id: str,
                        timeline_id: str = None):
        """Returns material request asynchronously

        :header_id: Material ID
        :app_id: Application ID
        :timeline_id: Timeline ID
        :returns: Material request

        """
        return await self.client.raw_api.get(
            f"Material/RequestPage?headerId={header_id}&pageId={app_id}" +
            (f"&timelineId={timeline_id}" if timeline_id else ""))

    async def app_request_form_update(self, header_id: str, app_id: str,
                                timeline_id: str, fields):
        """Updates material request form asynchronously

        :header_id: Material ID
        :app_id: Application ID
        :timeline_id: Timeline ID
        :fields: Dictionary of fields {'field_id':'field_value'}
        :returns: Updated material request

        """

        return await self.client.raw_api.post(
            f"Material/RequestPageForm?headerId={header_id}" +
            f"&pageId={app_id}&timelineId={timeline_id}",
            body=[{
                'id': field_id,
                'value': fields[field_id]
            } for field_id in fields])