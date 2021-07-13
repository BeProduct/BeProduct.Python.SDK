"""
File: _color.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: BeProduct Public API color methods
"""

from .sdk import BeProduct
from ._common_upload import UploadMixin
from ._common import CommonMixin


class Color(UploadMixin, CommonMixin):
    """
    Implements color API
    """

    def __init__(self, client: BeProduct):
        self.client = client
        UploadMixin.__init__(self, master_folder='color')
        CommonMixin.__init__(self, master_folder='color')

    def attributes_update(self, header_id: str, fields=None, colors=None):
        """Updates color attributes

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

        return self.client.raw_api.post(
            f"color/Header/{header_id}/Update",
            {
                'fields': unwound_attributes_fields,
                'colors': colors
            })

    def update(self, header_id: str, fields=None, colors=None):
        """ Same as attributes_update method.
            Updates color Attributes
        :returns: Updated color attributes
        """
        return self.attributes_update(header_id=header_id,
                                      fields=fields,
                                      colors=colors)

    def create(self, fields, colors):
        """Creates new color palette

        :fields: Dictionary of fields {'field_id':'field_value'}
        :returns: dictionary of the created color attributes
        :colors: List of colors in the palette/attributes 
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
            'color/Header/Create',
            {
                'fields': unwound_attributes_fields,
                'colors': colors
            })
