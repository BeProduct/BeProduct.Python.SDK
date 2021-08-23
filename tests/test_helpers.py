"""
File: test_helpers.py
Author: Yuri Golub
Email: yuri.golub@winks.io
Github: https: // github.com/BeProduct
"""
import os
from time import sleep

if True:
    import sys
    sys.path.append('src')

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


def get_empty_trash_bin():
    return {
        'TMP_STYLE_IDS': []
    }


def cleanup(self):
    if 'TMP_STYLE_IDS' in self.trash_bin:
        for style_id in self.trash_bin['TMP_STYLE_IDS']:
            delete_tmp_style(self, style_id)


def create_tmp_style(self, style_folder_id=None):
    tmp_style = self.client.style.attributes_create(
        folder_id=style_folder_id or self.config.STYLE_FOLDER['id'],
        fields=self.config.TMP_STYLE_ATTRIBUTES_FIELDS)

    self.assertEquals(
        tmp_style,
        self.client.style.attributes_get(header_id=tmp_style['id']))

    self.trash_bin['TMP_STYLE_IDS'].append(tmp_style['id'])
    return tmp_style


def delete_tmp_style(self, style_id):
    self.client.style.attributes_delete(header_id=style_id)

    with self.assertRaisesRegex(Exception, 'Style not found'):
        self.client.style.attributes_get(header_id=style_id)


def check_upload_status(self, upload_id, attempts=20):
    attempt = 1
    while True:
        (is_finished, is_error, error_msg) = self.client.style.upload_status(
            upload_id=upload_id)
        if is_finished:
            return not is_error

        if attempt < attempts:
            attempt += 1
            sleep(3)
        else:
            return False
