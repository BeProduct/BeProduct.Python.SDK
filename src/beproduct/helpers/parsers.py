from copy import deepcopy
from .composable import composable


@composable
def header_parser(header_data):
    """
    Parse header data as a dictionary from the header API response
    """
    special_fields = (
        "headerData",
        "colorways",
        "sizeRange",
        "sizeClasses",
        "id",
        "tags",
    )

    if not header_data:
        return None

    result = {
        "id": header_data["id"],
        "colorways": {},
    }

    result.update(
        {f["id"]: deepcopy(f["value"]) for f in header_data["headerData"]["fields"]}
    )

    result.update(
        {k: v for k, v in header_data["headerData"].items() if k not in ["fields"]}
    )

    result.update({k: v for k, v in header_data.items() if k not in special_fields})

    return dict(sorted(result.items()))


@composable
def style_parser(style_data):
    """
    Parse style data as a dictionary from the style API response
    """

    if not style_data:
        return None

    result = {
        "id": style_data["id"],
        "colorways": {},
        "default_size_range": {},
        "size_classes": {},
    }

    special_fields = (
        "headerData",
        "sizeRange",
        "colorways",
        "sizeClasses",
    )

    result.update(
        {f["id"]: deepcopy(f["value"]) for f in style_data["headerData"]["fields"]}
    )

    result.update(
        {k: v for k, v in style_data["headerData"].items() if k not in ["fields"]}
    )

    result.update({k: v for k, v in style_data.items() if k not in special_fields})

    for size in style_data["sizeRange"] or []:
        result["default_size_range"][size["name"]] = deepcopy(size)

    for colorway in style_data["colorways"] or []:
        result["colorways"][colorway["colorNumber"]] = deepcopy(colorway)

    for size_class in style_data["sizeClasses"] or []:
        result["size_classes"][size_class["name"]] = {
            **size_class,
            "size_range": {
                size["name"]: deepcopy(size) for size in (size_class["sizeRange"] or [])
            },
        }

    return dict(sorted(result.items()))


@composable
def material_parser(material_data):
    """
    Parse material data as a dictionary from the style API response
    """

    if not material_data:
        return None

    result = {
        "id": material_data["id"],
        "colorways": {},
        "default_size_range": {},
        "suppliers": {},
    }

    special_fields = ("headerData", "sizeRange", "colorways", "suppliers")

    result.update(
        {f["id"]: deepcopy(f["value"]) for f in material_data["headerData"]["fields"]}
    )

    result.update(
        {k: v for k, v in material_data["headerData"].items() if k not in ["fields"]}
    )

    result.update({k: v for k, v in material_data.items() if k not in special_fields})

    for size in material_data["sizeRange"] or []:
        result["default_size_range"][size["name"]] = deepcopy(size)

    for colorway in material_data["colorways"] or []:
        result["colorways"][colorway["colorNumber"]] = deepcopy(colorway)

    for supplier in material_data["suppliers"] or []:
        result["suppliers"][supplier["Id"]] = deepcopy(supplier)

    return dict(sorted(result.items()))


@composable
def app_list_parser(app_list):
    """
    Parse app list as a dictionary from the app list API response
    """

    result = {}

    if not app_list:
        return result

    for app in app_list:
        result[app["title"].lower()] = app

    return result


@composable
def dict_to_eq_filter_parser(filters):
    """
    Parse filters as a dictionary from the filter API response
    """

    if not filters:
        return []

    def _get_field_value(field_value):
        operator = "Eq"

        if isinstance(field_value, list):
            if any("*" in value for value in field_value):
                operator = "Contains"
                field_value = [value.replace("*", "") for value in field_value]
            return operator, "■".join(field_value)

        if isinstance(field_value, str):
            if "*" in field_value:
                return operator, field_value.replace("*", "")

        if isinstance(field_value, dict):
            if "operator" in field_value:
                operator = field_value["operator"]
                field_value = field_value["value"]

        return operator, field_value

    return [
        {
            "field": field_id,
            "operator": op_and_val[0],
            "value": op_and_val[1],
        }
        for field_id, field_value in filters.items()
        if (op_and_val := _get_field_value(field_value)) or True
    ]


@composable
def parse_array_as_or_filter(filters):
    """
    Parse filters as a dictionary from the filter API response
    """

    if not filters:
        return []

    return [
        {
            **{
                fid: fval
                for fid, fval in fil.items()
                if not (fid == "type" and fval not in ["Date", "Boolean", "Number"])
                and fid in ["field", "operator", "type"]
            },
            "value": (
                fil["value"]
                if not isinstance(fil["value"], list)
                else "■".join(fil["value"])
            ),
        }
        for fil in filters
    ]
