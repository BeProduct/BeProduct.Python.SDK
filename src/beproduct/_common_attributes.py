"""
File: _common_attributes.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: Attributes Mixin for every master folder
"""


class AttributesMixin:
    """
    Attributes mixin class for every master folder
    """

    def folders(self):
        """
        :returns: List of folders
        """
        return self.client.raw_api.get(f"{self.master_folder}/Folders")

    def folder_schema(self, folder_id: str):
        """Gets attributes schema (list of fields ) for a folder

        :folder_id: ID of the folder
        :returns: Attributes schema

        """
        return self.client.raw_api.get(
            f"{self.master_folder}/FolderSchema?folderId={folder_id}"
        )

    # ATTRIBUTES

    def attributes_list(
        self,
        folder_id: str = "",
        filters=None,
        colorway_filters=None,
        page_size=30,
        **kwargs,
    ):
        """List of attributes
        :folder_id: Folder ID
        :filters: List of filter dictionaries
        :colorway_filters: List of colorway filter dictionaries
        :**kwargs: Additional url parameters
        :returns: Enumerator of Attributes
        """

        # Convert filters to the format that the API expects
        _filters = []
        if filters:
            for f in filters:
                _filters.append(
                    {
                        **f,
                        "value": (
                            "■".join(f["value"])
                            if isinstance(f["value"], list)
                            else f["value"]
                        ),
                    }
                )

        return self.client.beproduct_paging_iterator(
            page_size,
            lambda psize, pnum: self.client.raw_api.post(
                f"{self.master_folder}/Headers?folderId={folder_id}"
                + f"&pageSize={psize}&pageNumber={pnum}",
                body={"filters": _filters, "colorwayFilters": colorway_filters},
                **kwargs,
            ),
        )

    def attributes_get(self, header_id: str, **kwargs):
        """Returns style attibutes

        :header_id: ID of the style, material, image etc.
        :**kwargs: Additional url parameters
        :returns: dictionary of the requested style attributes

        """
        return self.client.raw_api.get(
            f"{self.master_folder}/Header/{header_id}", **kwargs
        )

    def attributes_delete(self, header_id: str, **kwargs):
        """Deletes Style/Material/Image by ID

        :header_id: ID of the Style/Material/Image
        :**kwargs: Additional url parameters
        :returns:
        """
        return self.client.raw_api.get(
            f"{self.master_folder}/Header/Delete/{header_id}", **kwargs
        )

    def attributes_get_by_number(self, header_number: str, **kwargs):
        """Returns style attibutes by number

        :header_number: Number of the style, material, image etc.
        :**kwargs: Additional url parameters
        :returns: dictionary of the requested style attributes
        """

        return next(
            self.attributes_list(
                filters=[
                    {"field": "header_number", "operator": "Eq", "value": header_number}
                ]
            ),
            None,
        )
