"""
File: _style_async.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: BeProduct Public API Style methods - Async Version
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

class StyleAsync(
    UploadMixinAsync,
    AttributesMixinAsync,
    AppsMixinAsync,
    CommentsMixinAsync,
    RevisionsMixinAsync,
    ShareMixinAsync,
    TagsMixinAsync,
):
    """
    Implements Style API - Async Version
    """

    def __init__(self, client: BeProductAsync):
        """Constructor
        :param client: AsyncBeProduct instance
        """
        self.client = client
        self.master_folder = "Style"

    async def folder_colorway_schema(self, folder_id: str) -> Dict[str, Any]:
        """Gets colorway schema (list of fields) for a folder

        :param folder_id: ID of the folder
        :returns: Colorway schema
        """
        return await self.client.raw_api.get(f"Style/ColorwaySchema?folderId={folder_id}")

    # ATTRIBUTES

    async def attributes_update(
        self,
        header_id: str,
        fields: Optional[Dict[str, Any]] = None,
        colorways: Optional[List[Dict[str, Any]]] = None,
        sizes: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Updates style attributes

        :param header_id: ID of the style
        :param fields: Dictionary of fields {'field_id':'field_value'}
        :param colorways: Dictionary in Colorway update format
        :param sizes: Dictionary in Size format
        :returns: dictionary of the requested style attributes
        """
        # Transform attributes dictionary
        unwound_attributes_fields = []
        if fields:
            for field_id in fields:
                unwound_attributes_fields.append(
                    {"id": field_id, "value": fields[field_id]}
                )

        # Transform colorway dictionary
        colorway_fields = []
        if colorways:
            for color in colorways:
                unwound_colorway_fields = []
                for field_id in color["fields"]:
                    unwound_colorway_fields.append(
                        {"id": field_id, "value": color["fields"][field_id]}
                    )
                colorway_fields.append(
                    {"id": color["id"], "fields": unwound_colorway_fields}
                )

        return await self.client.raw_api.post(
            f"Style/Header/{header_id}/Update",
            {
                "fields": unwound_attributes_fields,
                "colorways": colorway_fields,
                "sizes": sizes,
            },
        )

    async def attributes_create(
        self,
        folder_id: str,
        fields: Dict[str, Any],
        colorways: Optional[List[Dict[str, Any]]] = None,
        sizes: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Creates new style

        :param folder_id: ID of the folder to create style in
        :param fields: Dictionary of fields {'field_id':'field_value'}
        :param colorways: Dictionary of colorway fields
        :param sizes: Dictionary in Size format
        :returns: dictionary of the created style attributes
        """
        # Transform attributes dictionary
        unwound_attributes_fields = []
        for field_id in fields:
            unwound_attributes_fields.append(
                {"id": field_id, "value": fields[field_id]}
            )

        # Transform colorway dictionary
        colorway_fields = []
        if colorways:
            for color in colorways:
                unwound_colorway_fields = []
                for field_id in color["fields"]:
                    unwound_colorway_fields.append(
                        {"id": field_id, "value": color["fields"][field_id]}
                    )
                colorway_fields.append(
                    {"id": color["id"], "fields": unwound_colorway_fields}
                )

        return await self.client.raw_api.post(
            f"Style/Header/Create?folderId={folder_id}",
            {
                "fields": unwound_attributes_fields,
                "colorways": colorway_fields,
                "sizes": sizes,
            },
        )

    async def attributes_colorway_delete(self, header_id: str, colorway_id: str) -> Dict[str, Any]:
        """Deletes single colorway from Attributes app

        :param header_id: Style ID
        :param colorway_id: ID of the colorway to be deleted
        :returns: Response from the API
        """
        return await self.client.raw_api.get(
            f"Style/Header/{header_id}/Colorway/Delete/{colorway_id}"
        )

    async def attributes_colorway_upload(
        self,
        header_id: str,
        colorway_id: Optional[str] = None,
        filepath: Optional[str] = None,
        fileurl: Optional[str] = None,
        color_number: Optional[str] = None,
    ) -> str:
        """Uploads colorway image

        :param header_id: Style ID
        :param colorway_id: Colorway ID
        :param color_number: Color number
        :param filepath: Local file path
        :param fileurl: Remote file URL
        :returns: Upload ID
        """
        if filepath:
            return await self.client.raw_api.upload_local_file(
                filepath,
                f"Style/Header/{header_id}/ColorwayImage/Upload?"
                + f"colorNumber={color_number}&colorId={colorway_id}",
            )
        if fileurl:
            return await self.client.raw_api.upload_from_url(
                fileurl,
                f"Style/Header/{header_id}/ColorwayImage/Upload?"
                + f"colorNumber={color_number}&colorId={colorway_id}",
            )

        raise BeProductException("No file provided")

    # APPS

    async def app_sku_generate(self, header_id: str, app_id: str) -> Dict[str, Any]:
        """Populates SKU with actual data from Attributes app

        :param header_id: ID of the Style
        :param app_id: App ID
        :returns: SKU app dictionary
        """
        return await self.client.raw_api.post(f"Style/Sku/{header_id}/{app_id}/Generate", {})

    async def app_sku_update(
        self,
        header_id: str,
        app_id: str,
        fields: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Updates fields in individual SKU rows

        :param header_id: ID of the Style
        :param app_id: App ID
        :param fields: Fields dictionary
        :returns: SKU app dictionary
        """
        return await self.client.raw_api.post(
            f"Style/Sku/{header_id}/{app_id}/Update", fields
        )

    async def app_artboard_version_upload(
        self,
        header_id: str,
        filepath: Optional[str] = None,
        fileurl: Optional[str] = None
    ) -> str:
        """Uploads an image as a new version into Artboard application

        :param header_id: Style ID
        :param filepath: Local file path
        :param fileurl: Remote file URL
        :returns: Upload ID
        """
        if filepath:
            return await self.client.raw_api.upload_local_file(
                filepath, f"Style/Header/{header_id}/Image/Upload"
            )
        if fileurl:
            return await self.client.raw_api.upload_from_url(
                fileurl, f"Style/Header/{header_id}/Image/Upload"
            )

        raise BeProductException("No file provided")

    async def app_bom_update(
        self,
        header_id: str,
        app_id: str,
        rows: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Updates BOM rows

        :param header_id: ID of the Style
        :param app_id: App ID
        :param rows: List of row dictionaries
        :returns: BOM app dictionary
        """
        return await self.client.raw_api.post(
            f"Style/Bom/{header_id}/{app_id}/Update", rows
        )

    async def app_request_list(self, header_id: str) -> List[Dict[str, Any]]:
        """Gets list of requests for a style

        :param header_id: ID of the Style
        :returns: List of requests
        """
        return await self.client.raw_api.get(f"Style/Request/{header_id}/List")

    async def app_request_get(
        self,
        header_id: str,
        app_id: str,
        timeline_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Gets request form data

        :param header_id: ID of the Style
        :param app_id: App ID
        :param timeline_id: Timeline ID
        :returns: Request form data
        """
        url = f"Style/Request/{header_id}/{app_id}"
        if timeline_id:
            url += f"/{timeline_id}"
        return await self.client.raw_api.get(url)

    async def app_request_form_update(
        self,
        header_id: str,
        app_id: str,
        timeline_id: str,
        fields: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Updates request form data

        :param header_id: ID of the Style
        :param app_id: App ID
        :param timeline_id: Timeline ID
        :param fields: Fields dictionary
        :returns: Updated request form data
        """
        return await self.client.raw_api.post(
            f"Style/Request/{header_id}/{app_id}/{timeline_id}/Update", fields
        )

    async def app_3D_style_turntable_upload(
        self,
        header_id: str,
        version_id: Optional[str] = None,
        replace_images: bool = False,
        filepath: Optional[str] = None,
        fileurl: Optional[str] = None,
    ) -> str:
        """Uploads turntable images

        :param header_id: Style ID
        :param version_id: Version ID
        :param replace_images: Whether to replace existing images
        :param filepath: Local file path
        :param fileurl: Remote file URL
        :returns: Upload ID
        """

        query = ""
        if version_id:
            query += f"versionId={version_id}&"
        if replace_images:
            query += "replaceImages=true&"

        if filepath:
            return await self.client.raw_api.upload_local_file(
                filepath,
                f"Style/Header/{header_id}/Image/Upload/Turntable?"
                + (query if query else ""),
            )
        if fileurl:
            return await self.client.raw_api.upload_from_url(
                fileurl,
                f"Style/Header/{header_id}/Image/Upload/Turntable?"
                + (query if query else ""),
            )

        return BeProductException("No file provided")

    async def app_3D_style_version_create(
        self,
        header_id: str,
        app_id: str,
        version_name: str
    ) -> Dict[str, Any]:
        """Creates new 3D version

        :param header_id: Style ID
        :param app_id: App ID
        :param version_name: Version name
        :returns: Created version object
        """
        return await self.client.raw_api.post(
            f"Style/3D/{header_id}/{app_id}/Version/Create",
            {"name": version_name}
        )

    async def app_3D_style_version_copy(
        self,
        header_id: str,
        app_id: str,
        copy_from_version_id: str,
        version_name: str
    ) -> Dict[str, Any]:
        """Copies 3D version

        :param header_id: Style ID
        :param app_id: App ID
        :param copy_from_version_id: Source version ID
        :param version_name: New version name
        :returns: Created version object
        """
        return await self.client.raw_api.post(
            f"Style/{header_id}/" + f"Page3DStyle/{app_id}/CreateVersion",
            body={"copyVersionId": copy_from_version_id, "versionName": version_name},
        )

    async def app_3D_style_version_delete(
        self,
        header_id: str,
        app_id: str,
        version_id: str
    ) -> None:
        """Deletes 3D version

        :param header_id: Style ID
        :param app_id: App ID
        :param version_id: Version ID
        """
        return await self.client.raw_api.delete(
            f"Style/{header_id}/" + f"Page3DStyle/{app_id}/Version/{version_id}"
        )

    async def app_3D_style_version_update(
        self,
        header_id: str,
        app_id: str,
        version_id: str,
        version_update: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Updates 3D version

        :param header_id: Style ID
        :param app_id: App ID
        :param version_id: Version ID
        :param version_update: Update data
        :returns: Updated version object
        """
        return await self.client.raw_api.post(
            f"Style/{header_id}/" + f"Page3DStyle/{app_id}/Version/{version_id}/Update",
            body=version_update,
        )

    async def app_3D_style_working_file_upload(
        self,
        header_id: str,
        app_id: str,
        version_id: str,
        filepath: Optional[str] = None,
        fileurl: Optional[str] = None,
    ) -> str:
        """Uploads 3D working file

        :param header_id: Style ID
        :param app_id: App ID
        :param version_id: Version ID
        :param filepath: Local file path
        :param fileurl: Remote file URL
        :returns: Upload ID
        """
        if filepath:
            return await self.client.raw_api.upload_local_file(
                filepath,
                f"Style/{header_id}/Page3DStyle/{app_id}/Version/"
                + f"{version_id}/WorkingFile/Upload",
            )
        if fileurl:
            return await self.client.raw_api.upload_from_url(
                fileurl,
                f"Style/{header_id}/Page3DStyle/{app_id}/Version/"
                + f"{version_id}/WorkingFile/Upload",
            )

        return BeProductException("No file provided")

    async def app_3D_style_preview_upload(
        self,
        header_id: str,
        app_id: str,
        version_id: str,
        colorway_id: str,
        filepath: Optional[str] = None,
        fileurl: Optional[str] = None,
    ) -> str:
        """Uploads 3D preview image

        :param header_id: Style ID
        :param app_id: App ID
        :param version_id: Version ID
        :param colorway_id: Colorway ID
        :param filepath: Local file path
        :param fileurl: Remote file URL
        :returns: Upload ID
        """
        if filepath:
            return await self.client.raw_api.upload_local_file(
                filepath,
                f"Style/{header_id}/Page3DStyle/{app_id}/Version/"
                + f"{version_id}/Colorway/{colorway_id}/Preview/Upload",
            )
        if fileurl:
            return await self.client.raw_api.upload_from_url(
                fileurl,
                f"Style/{header_id}/Page3DStyle/{app_id}/Version/"
                + f"{version_id}/Colorway/{colorway_id}/Preview/Upload",
            )

        return BeProductException("No file provided")
