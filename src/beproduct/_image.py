"""
File: _image.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: BeProduct Public API Image methods
"""

from .sdk import BeProduct
from ._common_upload import UploadMixin
from ._common import CommonMixin


class Image(UploadMixin, CommonMixin):
    """
    Implements Image API
    """

    def __init__(self, client: BeProduct):
        self.client = client
        UploadMixin.__init__(self, master_folder='Image')
        CommonMixin.__init__(self, master_folder='Image')

    def attributes_update(self, header_id: str, fields=None):
        """Updates image attributes

        :header_id: ID of the image
        :fields: Dictionary of fields {'field_id':'field_value'}
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

        return self.client.raw_api.post(
            f"Image/Header/{header_id}/Update",
            {
                'fields': unwound_attributes_fields
            })

    def attributes_create(
            self,
            folder_id: str,
            fields):
        """Creates new image

        :folder_id: ID of the folder to create in
        :fields: Dictionary of fields {'field_id':'field_value'}
        :returns: dictionary of the created image attributes
        """

        # transform attributes dictionary
        unwound_attributes_fields = []
        for field_id in fields:
            unwound_attributes_fields.append({
                'id': field_id,
                'value': fields[field_id]
            })

        return self.client.raw_api.post(
            f"Image/Header/Create?folderId={folder_id}",
            {
                'fields': unwound_attributes_fields
            })
