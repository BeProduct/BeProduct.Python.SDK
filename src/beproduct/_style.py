"""
File: _style.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: BeProduct Public API Style methods
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


class Style(
        UploadMixin,
        AttributesMixin,
        AppsMixin,
        CommentsMixin,
        RevisionsMixin,
        ShareMixin,
        TagsMixin):

    """
    Implements Style API
    """

    def __init__(self, client: BeProduct):
        self.client = client
        self.master_folder = 'Style'

    def folder_colorway_schema(self, folder_id: str):
        """Gets colorway schema (list of fields ) for a folder

        :folder_id: ID of the folder
        :returns: Colorway schema

        """
        return self.client.raw_api.get(
            f"Style/ColorwaySchema?folderId={folder_id}")

    # ATTRIBUTES

    def attributes_update(self,
                          header_id: str,
                          fields=None,
                          colorways=None,
                          sizes=None):
        """Updates style attributes

        :header_id: ID of the style
        :fields: Dictionary of fields {'field_id':'field_value'}
        :colorways Dictionary in Colorway update format
        :sizes Dictionary in Size format
        :returns: dictionary of the requested style attributes

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

        return self.client.raw_api.post(f"Style/Header/{header_id}/Update",
                                        {
                                            'fields': unwound_attributes_fields,
                                            'colorways': colorway_fields,
                                            'sizes': sizes
                                        })

    def attributes_create(
            self,
            folder_id: str,
            fields,
            colorways=None,
            sizes=None):
        """Creates new style

        :folder_id: ID of the folder to create style in
        :fields: Dictionary of fields {'field_id':'field_value'}
        :colorways Dictionary of colorway fields
        :sizes Dictionary in Size format
        :returns: dictionary of the created style attributes
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

        return self.client.raw_api.post(
            f"Style/Header/Create?folderId={folder_id}",
            {
                'fields': unwound_attributes_fields,
                'colorways': colorway_fields,
                'sizes': sizes
            })

    def attributes_colorway_delete(self, header_id: str, colorway_id: str):
        """Deletes single colorway from Attributes app

        :header_id: Style ID
        :colorway_id: ID of the colorway to be deleted

        """
        return self.client.raw_api.get(
            f"Style/Header/{header_id}/Colorway/Delete/{colorway_id}")

    def attributes_colorway_upload(
            self,
            header_id: str,
            colorway_id: str = None,
            filepath: str = None,
            fileurl: str = None,
            color_number: str = None):
        """Uploads colorway image
        :header_id: Style ID
        :colorway_id: Colorway ID
        :color_number: Color number
        :filepath: Local file path
        :fileurl: Remote file URL
        :returns: Upload ID

        """
        if filepath:
            return self.client.raw_api.upload_local_file(
                filepath,
                f"Style/Header/{header_id}/ColorwayImage/Upload?" +
                f"colorNumber={color_number}&colorId={colorway_id}")
        if fileurl:
            return self.client.raw_api.upload_from_url(
                fileurl,
                f"Style/Header/{header_id}/ColorwayImage/Upload?" +
                f"colorNumber={color_number}&colorId={colorway_id}")

        return BeProductException("No file provided")

    # APPS

    def app_sku_generate(self, header_id: str, app_id: str):
        """Populates SKU with actual data from Attributes app

        :header_id: ID of the Style
        :app_id: App ID
        :returns: SKU app dictionary

        """
        return self.client.raw_api.post(
            f"Style/Sku/{header_id}/{app_id}/Generate", {})

    def app_sku_update(self, header_id, app_id, fields):
        """Updates fields in individual SKU rows

        :header_id: ID of the Style
        :app_id: App ID
        :fields: Fields dictionary
        :returns: SKU app dictionary

        """
        return self.client.raw_api.post(
            f"Style/Sku/PageSku?headerId={header_id}&pageId={app_id}",
            body=fields)

    def app_artboard_version_upload(
            self,
            header_id: str,
            filepath: str = None,
            fileurl: str = None):
        """Uploads an image as a new version into Artboard application

        :header_id: Style ID
        :filepath: Local file path
        :fileurl: Remote file URL
        :returns: Upload ID

        """
        if filepath:
            return self.client.raw_api.upload_local_file(
                filepath, f"Style/Header/{header_id}/Image/Upload")
        if fileurl:
            return self.client.raw_api.upload_from_url(
                fileurl, f"Style/Header/{header_id}/Image/Upload")

        return BeProductException("No file provided")

    def app_3D_style_turntable_upload(
            self,
            header_id: str,
            filepath: str = None,
            fileurl: str = None):
        """Uploads new turntable version into 3D style app

        :header_id: Style ID
        :filepath: Local file path
        :fileurl: Remote file URL
        :returns: Upload ID

        """
        if filepath:
            return self.client.raw_api.upload_local_file(
                filepath,
                f"Style/Header/{header_id}/Image/Upload/Turntable" +
                + "?updateHeader=false")
        if fileurl:
            return self.client.raw_api.upload_from_url(
                fileurl,
                f"Style/Header/{header_id}/Image/Upload/Turntable" +
                + "?updateHeader=false")

        return BeProductException("No file provided")

    def app_bom_update(self, header_id: str, app_id: str, rows):
        """ Updates BOM application
        :header_id: ID of the style, material, etc
        :app_id: ID of the application / page
        :row: List of row/material dictionaries
        """

        return self.client.raw_api.post(
            f"Style/PageCBOM?headerId={header_id}&pageId={app_id}",
            body=rows)

    def app_request_list(self, header_id: str):
        """ List of request apps

        :header_id: Style ID
        :returns: List of Style Request Applications

        """
        return self.client.raw_api.get(
            f"Style/RequestPages?headerId={header_id}")

    def app_request_get(self, header_id: str, app_id: str, timeline_id: str = None):
        """TODO: Docstring for app_request_get.

        :header_id: Style ID
        :app_id: App ID
        :timeline_id: (Optional) Plan Timeline ID if you need a specific app record
        :returns: List of Request Apps for all plan timelines where app exists

        """

        return self.client.raw_api.get(
            f"Style/RequestPage?headerId={header_id}&pageId={app_id}" +
            (f"&timelineId={timeline_id}" if timeline_id else ""))

    def app_request_form_update(
            self,
            header_id: str,
            app_id: str,
            timeline_id: str,
            fields):
        """ Updates form application
        :header_id: ID of the style, material, etc
        :app_id: ID of the application / page
        :timeline_id: Plan Timeline Id
        :fields: Dictionary of fields to update {'field_id':'value'}
        """
        return self.client.raw_api.post(
            f"Style/RequestPageForm?headerId={header_id}" +
            f"&pageId={app_id}&timelineId={timeline_id}",
            body=[{'id': field_id, 'value': fields[field_id]}
                  for field_id in fields])
