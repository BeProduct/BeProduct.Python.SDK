from copy import deepcopy
from .composable import composable


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

    return [
        {
            "field": field_id,
            "operator": "eq",
            "value": (
                "■".join(field_value) if isinstance(field_value, list) else field_value
            ),
        }
        for field_id, field_value in filters.items()
    ]
