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
from ._exception import BeProductException


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

    def attributes_create(self, fields, colorways, sizes, suppliers):
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
            'Material/Header/Create',
            {
                'fields': unwound_attributes_fields,
                'colorways': colorway_fields,
                'sizes': sizes,
                'suppliers': suppliers
            })

    def attributes_colorway_delete(self, header_id: str, colorway_id: str):
        """Deletes single colorway from Attributes app

        :header_id: Material ID
        :colorway_id: ID of the colorway to be deleted

        """
        return self.client.raw_api.get(
            f"Material/Header/{header_id}/Colorway/Delete/{colorway_id}")

    def attributes_colorway_upload(
            self,
            header_id: str,
            colorway_id: str = None,
            filepath: str = None,
            fileurl: str = None,
            color_number: str = None):
        """Uploads colorway image
        :header_id: Material ID
        :colorway_id: Colorway ID
        :color_number: Color number
        :filepath: Local file path
        :fileurl: Remote file URL
        :returns: File ID

        """
        if filepath:
            return self.client.raw_api.upload_local_file(
                filepath,
                f"Material/Header/{header_id}/ColorwayImage/Upload?" +
                f"colorNumber={color_number}&colorId={colorway_id}")
        if fileurl:
            return self.client.raw_api.upload_from_url(
                fileurl,
                f"Material/Header/{header_id}/ColorwayImage/Upload?" +
                f"colorNumber={color_number}&colorId={colorway_id}")

        return BeProductException("No file provided")

    # APPS

    def app_artboard_version_upload(
            self,
            header_id: str,
            filepath: str = None,
            fileurl: str = None):
        """Uploads an image as a new version into Artboard application

        :header_id: Material ID
        :filepath: Local file path
        :fileurl: Remote file URL
        :returns: File ID

        """
        if filepath:
            return self.client.raw_api.upload_local_file(
                filepath, f"Material/Header/{header_id}/Image/Upload")
        if fileurl:
            return self.client.raw_api.upload_from_url(
                fileurl, f"Material/Header/{header_id}/Image/Upload")

        return BeProductException("No file provided")
