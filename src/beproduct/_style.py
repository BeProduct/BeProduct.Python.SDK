"""
File: _style.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: BeProduct Public API Style methods
"""


def style_attributes_get(self, style_id: str):
    """Returns style attibutes

    :style_id: Style ID - GUID string
    :returns: dictionary of the requested style attributes

    """
    return self.get(f"Style/Header/{style_id}")
