"""
File: _helpers.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: Helper methods
"""


def beproduct_paging_iterator(page_size: int, page_func):
    """
    Yields iterator of BeProduct result pages
    """
    total = 0
    processed = 0
    page_number = 0

    while True:
        page = page_func(page_size, page_number)
        total = page['total']

        for attr in page['result']:
            processed += 1
            yield attr

        if processed >= total:
            break

        page_number += 1
