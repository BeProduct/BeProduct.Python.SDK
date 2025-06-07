"""
File: _user.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: User Public API
"""

from .sdk import BeProduct, BeProductAsync
from datetime import datetime


class Schema:
    """Implements User API"""

    def __init__(self, client: BeProduct | BeProductAsync):
        """Constructor"""
        self.client = client
        if isinstance(self.client, BeProductAsync):
            self.get_folder_schema = self._get_folder_schema_async
        else:
            self.get_folder_schema = self._get_folder_schema_sync

    def _get_folder_schema_sync(self, master_folder: str, folder_id: str):
        schema = self.client.raw_api.get(
            f"{master_folder}/FolderSchema?folderId={folder_id}"
        )
        return self._process_schema(schema, master_folder, folder_id)

    async def _get_folder_schema_async(self, master_folder: str, folder_id: str):
        schema = await self.client.raw_api.get(
            f"{master_folder}/FolderSchema?folderId={folder_id}"
        )
        return self._process_schema(schema, master_folder, folder_id)

    def _process_schema(self, schema: list, master_folder: str, folder_id: str):
        """Get folder schema

        :master_folder: master folder
        :folder_id: folder id
        :returns: folder schema

        """

        fields = []

        for field in schema or []:

            field_id = field.get("fieldId")
            field_name = field.get("fieldName")
            field_type = field.get("fieldType")
            required = field.get("required")
            properties = field.get("properties", {})
            formula = ""
            possible_values = []

            data_type = str

            if field_type in [
                "Text",
                "UserLabel",
                "LabelSize",
                "Memo",
                "Measure",
            ]:
                data_type = str

            elif field_type in ["TrueFalse", "Label3dMaterial", "Label3dStyle"]:
                data_type = bool

            elif field_type in [
                "LabelMaterial",
                "LabelStyleGroup",
                "FormulaField",
                "LabelText",
            ]:
                data_type = str
                formula = field.get("properties", {}).get("Formula", "")

            elif field_type in ["DateTime", "Date"]:
                data_type = datetime

            elif field_type in ["Decimal", "Percent", "Currency", "Weight"]:
                data_type = float

            elif field_type in ["DropDown", "MultiSelect", "ComboBox"]:
                data_type = list
                possible_values = [
                    {
                        "id": choice.get("id") if type(choice) is dict else "",
                        "code": choice.get("code") if type(choice) is dict else "",
                        "value": (
                            choice.get("value") if type(choice) is dict else choice
                        ),
                    }
                    for choice in field.get("properties", {}).get("Choices", [])
                ]
            elif field_type in ["Number"]:
                data_type = int

            elif field_type in ["CompositeControl"]:
                data_type = list
                possible_values = [
                    {
                        "id": v,
                        "code": v,
                        "value": v,
                    }
                    for v in field.get("properties", {}).get("Choices", "").split("\n")
                ]

            elif field_type in ["PartnerDropDown"]:
                data_type = list
                possible_values = [
                    {
                        "id": choice.get("code"),
                        "code": choice.get("code"),
                        "value": choice.get("value"),
                    }
                    for choice in field.get("properties", {}).get("Choices", [])
                ]

            elif field_type in ["Users"]:
                data_type = str

            elif field_type in ["MultiSelect"]:
                data_type = list

            else:
                ...
                # assert False, f"Unknown field type: {field_type}"

            fields.append(
                {
                    "field_id": field_id,
                    "field_name": field_name,
                    "field_type": field_type,
                    "required": required,
                    "formula": formula,
                    "possible_values": possible_values,
                    "data_type": data_type,
                    "properties": properties,
                }
            )

        fields.append(
            {
                "field_id": "ModifiedAt",
                "field_name": "Modified Date",
                "field_type": "DateTime",
                "required": False,
                "formula": "",
                "possible_values": [],
                "data_type": datetime,
                "properties": {},
            }
        )
        return fields

    def get_style_folder_schema(self, folder_id: str):
        """Get style folder schema

        :folder_id: folder id
        :returns: style folder schema

        """
        return self._get_folder_schema("Style", folder_id)

    def get_material_folder_schema(self, folder_id: str):
        """Get material folder schema

        :folder_id: folder id
        :returns: material folder schema

        """
        return self._get_folder_schema("Material", folder_id)

    def get_color_folder_schema(self, folder_id: str):
        """Get color folder schema

        :folder_id: folder id
        :returns: color folder schema

        """
        return self._get_folder_schema("Color", folder_id)
