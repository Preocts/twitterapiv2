import os
from typing import Any
from typing import Dict
from unittest.mock import patch

import pytest
from twitterapiv2.userauth_client import UserAuthClient

MOCK_VALUES: Dict[str, Any] = {
    "method": "post",
    "route": "/1.1/statuses/update.json",
    "fields": {
        "include_entities": "true",
        "status": "Hello Ladies + Gentlemen, a signed OAuth request!",
    },
    "oauth_nonce": "kYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg",
    "oauth_timestamp": "1318622958",
    "expected_parameter_string": (
        "include_entities=true&oauth_consumer_key=xvz1evFS4wEEPTGEFPHBog&"
        "oauth_nonce=kYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg&"
        "oauth_signature_method=HMAC-SHA1&oauth_timestamp=1318622958&"
        "oauth_token=370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb&"
        "oauth_version=1.0&status=Hello%20Ladies%20%2B%20Gentlemen%2C%20a%20"
        "signed%20OAuth%20request%21"
    ),
    "expected_base_string": (
        "POST&https%3A%2F%2Fapi.twitter.com%2F1.1%2Fstatuses%2Fupdate.json&"
        "include_entities%3Dtrue%26oauth_consumer_key%3Dxvz1evFS4wEEPTGEFPHBog%26"
        "oauth_nonce%3DkYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg%26"
        "oauth_signature_method%3DHMAC-SHA1%26oauth_timestamp%3D1318622958%26"
        "oauth_token%3D370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb%26"
        "oauth_version%3D1.0%26status%3DHello%2520Ladies%2520%252B%2520Gentlemen"
        "%252C%2520a%2520signed%2520OAuth%2520request%2521"
    ),
    "expected_signature": "hCtSmYh+iHYCEqBWrE7C7hYmtUk=",
    "expected_header": (
        'OAuth oauth_consumer_key="xvz1evFS4wEEPTGEFPHBog", '
        'oauth_nonce="kYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg", '
        'oauth_signature="tnnArxj06cWHq44gCs1OSKk%2FjLY%3D", '
        'oauth_signature_method="HMAC-SHA1", '
        'oauth_timestamp="1318622958", '
        'oauth_token="370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb", '
        'oauth_version="1.0"'
    ),
}
MOCK_HEADER_VALUES = {
    "oauth_consumer_key": "xvz1evFS4wEEPTGEFPHBog",
    "oauth_nonce": "kYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg",
    "oauth_signature": "tnnArxj06cWHq44gCs1OSKk/jLY=",
    "oauth_signature_method": "HMAC-SHA1",
    "oauth_timestamp": "1318622958",
    "oauth_token": "370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb",
    "oauth_version": "1.0",
}
MOCK_TOKENS = {
    "TW_CONSUMER_KEY": "xvz1evFS4wEEPTGEFPHBog",
    "TW_ACCESS_TOKEN": "370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb",
    "TW_CONSUMER_SECRET": "kAcSOqF21Fu85e7zjz7ZN2U4ZRhfV3WpwPAoE3Z7kBw",
    "TW_ACCESS_SECRET": "LswwdoUaIvS8ltyTt5jkRh4J50vUPVVHtR2YPi5kE",
}


def test_key_collect() -> None:
    client = UserAuthClient()
    assert client.generate_header_key_values()


def test_key_collect_raises() -> None:
    client = UserAuthClient()
    with patch.dict(os.environ):
        del os.environ["TW_CONSUMER_KEY"]
        with pytest.raises(KeyError):
            client.generate_header_key_values()


def test_generate_paramter_string() -> None:
    client = UserAuthClient()
    with patch.dict(os.environ, MOCK_TOKENS):
        keys = client.generate_header_key_values()
        keys["oauth_nonce"] = MOCK_VALUES["oauth_nonce"]
        keys["oauth_timestamp"] = MOCK_VALUES["oauth_timestamp"]
        parameter_string = client.generate_parameter_string(
            fields={**keys, **MOCK_VALUES["fields"]}
        )
    assert parameter_string == MOCK_VALUES["expected_parameter_string"]


def test_generate_signature_base_string() -> None:
    client = UserAuthClient()
    parameter_string = MOCK_VALUES["expected_parameter_string"]
    base_string = client.generate_base_string(
        method=MOCK_VALUES["method"],
        route=MOCK_VALUES["route"],
        parameter_string=parameter_string,
    )
    assert base_string == MOCK_VALUES["expected_base_string"]


def test_generate_signature_string() -> None:
    client = UserAuthClient()
    base_string = MOCK_VALUES["expected_base_string"]
    with patch.dict(os.environ, MOCK_TOKENS):
        signature = client.generate_signature_string(base_string)
    assert signature == MOCK_VALUES["expected_signature"]


def test_generate_signature_string_raises() -> None:
    client = UserAuthClient()
    with patch.dict(os.environ):
        del os.environ["TW_CONSUMER_SECRET"]
        with pytest.raises(KeyError):
            client.generate_signature_string("")


def test_generate_oauth_header() -> None:
    client = UserAuthClient()
    header = client.generate_oauth_header(MOCK_HEADER_VALUES)
    assert header == MOCK_VALUES["expected_header"]
