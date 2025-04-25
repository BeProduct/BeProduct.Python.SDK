"""
File: _helpers_async.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: Async helper methods
"""


async def beproduct_paging_iterator_async(page_size: int, page_func):
    """
    Yields async iterator of BeProduct result pages
    """
    total = 0
    processed = 0
    page_number = 0

    while True:
        page = await page_func(page_size, page_number)
        total = page['total']

        for attr in page['result']:
            processed += 1
            yield attr

        if processed >= total:
            break

        page_number += 1 