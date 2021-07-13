"""
File: _style.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: BeProduct Public API Style methods
"""

from .sdk import BeProduct
from ._common_upload import UploadMixin
from ._common import CommonMixin


class Style(UploadMixin, CommonMixin):
    """
    Implements Style API
    """

    def __init__(self, client: BeProduct):
        self.client = client
        UploadMixin.__init__(self, master_folder='Style')
        CommonMixin.__init__(self, master_folder='Style')

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

    def update(self,
               header_id: str,
               fields=None,
               colorways=None,
               sizes=None):
        """ Same as attributes_update method. 
            Updates Style Attributes
        :returns: Updated style attributes
        """
        return self.attributes_update(header_id=header_id,
                                      fields=fields,
                                      colorways=colorways,
                                      sizes=sizes)

    def create(self, fields, colorways, sizes):
        """Creates new style

        :fields: Dictionary of fields {'field_id':'field_value'}
        :colorways Dictionary of colorway fields
        :sizes Dictionary in Size format
        :returns: dictionary of the created style attributes
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

        return self.client.raw_api.post(
            'Style/Header/Create',
            {
                'fields': unwound_attributes_fields,
                'colorways': colorway_fields,
                'sizes': sizes
            })
