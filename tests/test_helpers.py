"""
File: test_helpers.py
Author: Yuri Golub
Email: yuri.golub@winks.io
Github: https: // github.com/BeProduct
"""
import os
import json
from time import sleep

if True:
    import sys

    sys.path.append("src")

from beproduct.sdk import BeProduct


def get_papi_url(env: str):
    if env == "prod":
        return (
            "https://developers.beproduct.com",
            "https://id.winks.io/ids/connect/token",
        )
    elif env == "stage":
        return (
            "https://prod-public-api-beproduct-eastus-staging.azurewebsites.net",
            "https://id.winks.io/ids/connect/token",
        )
    elif env == "dev":
        return (
            "https://dev-public-api-beproduct-eastus.azurewebsites.net",
            "https://id.winks.io/ids/connect/token",
        )
    elif env == "local":
        os.environ["CURL_CA_BUNDLE"] = ""
        return ("https://localhost:44317", "https://id.winks.io/ids/connect/token")
    else:
        return None


def get_beproduct_client(config) -> BeProduct:
    papi_url, token_url = get_papi_url(os.environ.get("BP_ENV", None) or "prod")
    client = BeProduct(
        client_id=config.CLIENT_ID,
        client_secret=config.CLIENT_SECRET,
        refresh_token=config.REFRESH_TOKEN,
        company_domain=config.COMPANY_DOMAIN,
        public_api_url=papi_url,
        token_endpoint=token_url,
    )
    return client


def get_first(lambda_cond, seq):
    filtered_list = list(filter(lambda_cond, seq))
    if len(filtered_list):
        return filtered_list[0]
    else:
        return None


def get_empty_trash_bin():
    return {"TMP_STYLE_IDS": []}


def cleanup(self):
    if "TMP_STYLE_IDS" in self.trash_bin:
        for style_id in self.trash_bin["TMP_STYLE_IDS"]:
            delete_tmp_style(self, style_id)


def create_tmp_style(self, style_folder_id=None):
    tmp_style = self.client.style.attributes_create(
        folder_id=style_folder_id or self.config.STYLE_FOLDER["id"],
        fields=self.config.TMP_STYLE_ATTRIBUTES_FIELDS,
    )

    self.assertEquals(
        tmp_style, self.client.style.attributes_get(header_id=tmp_style["id"])
    )

    self.trash_bin["TMP_STYLE_IDS"].append(tmp_style["id"])
    return tmp_style


def delete_tmp_style(self, style_id):
    self.client.style.attributes_delete(header_id=style_id)

    with self.assertRaisesRegex(Exception, "Style not found"):
        self.client.style.attributes_get(header_id=style_id)


def check_upload_status(self, upload_id, attempts=20):
    attempt = 1
    while True:
        (is_finished, is_error, error_msg) = self.client.style.upload_status(
            upload_id=upload_id
        )
        if is_finished:
            return not is_error

        if attempt < attempts:
            attempt += 1
            sleep(3)
        else:
            return False


def is_subset_or_equals(expected, actual):
    """Recursive subset finder"""

    if type(expected) != type(actual):
        return False, f"type of {actual} is not equals to the type of {expected}"

    match expected:
        case dict():
            for key in expected.keys():
                if key not in actual:
                    return False, f"Actual doesnt have expected key {key}"

            res = [is_subset_or_equals(v, actual[k]) for k, v in expected.items()]
            for success, msg in res:
                if not success:
                    return success, msg
            else:
                return True, ""

        case list():
            for expected_item in expected:
                found = False
                for actual_item in actual:
                    if is_subset_or_equals(expected_item, actual_item)[0]:
                        found = True
                        break
                if not found:
                    return found, f"Item {expected_item} is not found in {actual}"
            else:
                return True, ""

        case str():
            if expected and expected.startswith("https://"):
                res = actual.startswith(expected)
                if res:
                    return True, ""
                else:
                    return (
                        res,
                        f"Actual value {actual} doesnt start with expected {expected}",
                    )
            else:
                res = actual == expected
                if res:
                    return True, ""
                else:
                    return (
                        res,
                        f"Actual value {actual} is not equals to expected {expected}",
                    )

        case _:
            res = actual == expected
            if res:
                return True, ""
            else:
                return (
                    res,
                    f"Actual value {actual} is not equals to expected {expected}",
                )
