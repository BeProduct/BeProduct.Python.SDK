"""
File: _material.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: BeProduct Public API material methods
"""

from .sdk import BeProduct
from ._common_upload import UploadMixin
from ._common import CommonMixin


class Material(UploadMixin, CommonMixin):
    """
    Implements Material API
    """

    def __init__(self, client: BeProduct):
        self.client = client
        UploadMixin.__init__(self, master_folder='Material')
        CommonMixin.__init__(self, master_folder='Material')

    def attributes_update(self,
                          header_id: str,
                          fields=None,
                          colorways=None,
                          sizes=None,
                          suppliers=None):
        """Updates material attributes

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

        return self.client.raw_api.post(f"Material/Header/{header_id}/Update",
                                        {
                                            'fields': unwound_attributes_fields,
                                            'colorways': colorway_fields,
                                            'sizes': sizes,
                                            'suppliers': suppliers
                                        })

    def update(self, header_id: str):
        """ Same as attributes_update method. 
            Updates material Attributes
        :returns: Updated material attributes
        """
        return self.attributes_update(header_id=header_id)

    def create(self, fields, colorways, sizes, suppliers):
        """Creates new material

        :fields: Dictionary of fields {'field_id':'field_value'}
        :colorways Dictionary of colorway fields
        :sizes Dictionary in Size format
        :suppliers: List of supplier dictionaries
        :returns: dictionary of the created material attributes
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
            'material/Header/Create',
            {
                'fields': unwound_attributes_fields,
                'colorways': colorway_fields,
                'sizes': sizes,
                'suppliers': suppliers
            })
