"""
File: test_helpers.py
Author: Yuri Golub
Email: yuri.golub@winks.io
Github: https: // github.com/BeProduct
"""
import os

if True:
    import sys
    sys.path.append(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)), '../src'))

from beproduct.sdk import BeProduct


def get_beproduct_client(config) -> BeProduct:
    client = BeProduct(client_id=config.CLIENT_ID,
                       client_secret=config.CLIENT_SECRET,
                       refresh_token=config.REFRESH_TOKEN,
                       company_domain=config.COMPANY_DOMAIN)
    return client


def get_first(lambda_cond, seq):
    filtered_list = list(filter(lambda_cond, seq))
    if len(filtered_list):
        return filtered_list[0]
    else:
        return None
