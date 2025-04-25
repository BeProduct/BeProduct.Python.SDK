"""
File: _schema_async.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: BeProduct Schema API - Async Version
"""

from typing import Dict, Any, Optional, List, Type, Union
from datetime import datetime
from .sdk_async import BeProductAsync

class SchemaAsync:
    """Implements Schema API - Async Version"""

    def __init__(self, client: BeProductAsync):
        """Constructor
        :param client: AsyncBeProduct instance
        """
        self.client = client

    async def _get_folder_schema(self, master_folder: str, folder_id: str) -> List[Dict[str, Any]]:
        """Get folder schema

        :param master_folder: master folder
        :param folder_id: folder id
        :returns: folder schema
        """
        schema = await self.client.raw_api.get(
            f"{master_folder}/FolderSchema?folderId={folder_id}"
        )

        fields = []

        for field in schema or []:
            field_id = field.get("fieldId")
            field_name = field.get("fieldName")
            field_type = field.get("fieldType")
            required = field.get("required")
            properties = field.get("properties", {})
            formula = ""
            possible_values = []

            data_type: Type = str

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
                        "id": choice.get("id") if isinstance(choice, dict) else "",
                        "code": choice.get("code") if isinstance(choice, dict) else "",
                        "value": (
                            choice.get("value") if isinstance(choice, dict) else choice
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

    async def get_style_folder_schema(self, folder_id: str) -> List[Dict[str, Any]]:
        """Get style folder schema

        :param folder_id: folder id
        :returns: style folder schema
        """
        return await self._get_folder_schema("Style", folder_id)

    async def get_material_folder_schema(self, folder_id: str) -> List[Dict[str, Any]]:
        """Get material folder schema

        :param folder_id: folder id
        :returns: material folder schema
        """
        return await self._get_folder_schema("Material", folder_id)

    async def get_image_folder_schema(self, folder_id: str) -> List[Dict[str, Any]]:
        """Get image folder schema

        :param folder_id: folder id
        :returns: image folder schema
        """
        return await self._get_folder_schema("Image", folder_id)

    async def get_color_folder_schema(self, folder_id: str) -> List[Dict[str, Any]]:
        """Get color folder schema

        :param folder_id: folder id
        :returns: color folder schema
        """
        return await self._get_folder_schema("Color", folder_id)

    async def get_folder_schema(self, folder_name: str, folder_id: str) -> Dict[str, Any]:
        """
        Get folder schema
        :param type_name: Type name (style, material, image or color)
        :param folder_id: Folder ID
        :return: Schema dictionary
        :raises: ValueError if type_name or folder_id is empty or None
        """
        if not folder_name:
            raise ValueError("folder_name cannot be empty or None")
        if not folder_id:
            raise ValueError("folder_id cannot be empty or None")
        
        valid_types = ['style', 'material', 'image', 'color']
        if folder_name.lower() not in valid_types:
            raise ValueError(f"folder_name must be one of: {', '.join(valid_types)}")

        return await self._get_folder_schema(folder_name, folder_id)

