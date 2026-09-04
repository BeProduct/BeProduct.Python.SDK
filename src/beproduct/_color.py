"""
File: _color.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: BeProduct Public API color methods
"""

from .sdk import BeProduct

from ._common_upload import UploadMixin
from ._common_attributes import AttributesMixin
from ._common_apps import AppsMixin
from ._common_comments import CommentsMixin
from ._common_revisions import RevisionsMixin
from ._common_share import ShareMixin
from ._common_tags import TagsMixin


class Color(UploadMixin, AttributesMixin, AppsMixin, CommentsMixin,
            RevisionsMixin, ShareMixin, TagsMixin):
    """
    Implements color API
    """

    def __init__(self, client: BeProduct):
        self.client = client
        self.master_folder = 'Color'

    def attributes_update(self, header_id: str, fields=None, colors=None, replace_colors: bool = True):
        """Updates color attributes

        :header_id: ID of the color
        :fields: Dictionary of fields {'field_id':'field_value'}
        :colors: List of colors in the palette/attributes
        :replace_colors: When true, replaces all palette colors with those from the request. Otherwise, merges request colors into existing ones matched by ID or color number.
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

        return self.client.raw_api.post(f"color/Header/{header_id}/Update?replaceColors={str(replace_colors).lower()}", {
            'fields': unwound_attributes_fields,
            'colors': colors
        })

    def attributes_create(self, folder_id: str, fields, colors=None, force_version_update: bool = False):
        """Creates new color palette

        :folder_id: ID of the folder to create in
        :fields: Dictionary of fields {'field_id':'field_value'}
        :force_version_update: If true, the header version from fields will be applied on creation
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

        return self.client.raw_api.post(
            f"color/Header/Create?folderId={folder_id}&preserveVersion={str(force_version_update).lower()}", {
                'fields': unwound_attributes_fields,
                'colors': colors
            })

    def folder_color_chip_schema(self, folder_id: str):
        """Gets the color chip schema (list of fields) for a color folder

        :folder_id: ID of the folder
        :returns: Color chip schema

        """
        return self.client.raw_api.get(f"Color/ColorChipSchema?folderId={folder_id}")

    def company_colors(self, filters=None, page_size: int = 30):
        """Lists the company color library

        :filters: List of filter dictionaries
        :page_size: Page size
        :returns: Enumerator of colors

        """
        return self.client.beproduct_paging_iterator(
            page_size,
            lambda psize, pnum: self.client.raw_api.post(
                f"Color/CompanyColors?pageSize={psize}&pageNumber={pnum}", body={"filters": filters or []}
            ),
        )

