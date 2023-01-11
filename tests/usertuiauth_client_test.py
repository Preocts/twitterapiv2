from __future__ import annotations

import os
from collections.abc import Generator
from typing import Any
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from twitterapiv2.model.useroauthresponse import UserOAuthResponse
from twitterapiv2.usertuiauth_client import UserTUIAuthClient

MOCK_VALUES: dict[str, Any] = {
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
    "expected_header": {
        "Authorization": (
            'OAuth oauth_consumer_key="xvz1evFS4wEEPTGEFPHBog", '
            'oauth_nonce="kYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg", '
            'oauth_signature="tnnArxj06cWHq44gCs1OSKk%2FjLY%3D", '
            'oauth_signature_method="HMAC-SHA1", '
            'oauth_timestamp="1318622958", '
            'oauth_token="370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb", '
            'oauth_version="1.0"'
        )
    },
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

MOCK_RESPONSE = UserOAuthResponse("mocktoken", "mocksecret", "mock", "mock")
USER_RESP = "oauth_token=UsPAbAAAAAABVjj_AAABfYO81xo&oauth_token_secret=mwr3uC5LWlgfYewBMNVTAi1VPlI1BmXL&oauth_callback_confirmed=true"  # noqa
ACCESS_RESP = "oauth_token=1069768653757997056-8rVedS0KEQI9KvzLOtamAw0wZixSBB&oauth_token_secret=i3OCVHR0AGXjMrCcrBtedNi89vUm4YovBo67cE8Xaf4z8&user_id=1069768653757997&screen_name=preocts"  # noqa


@pytest.fixture(autouse=True)
def mask_environ() -> Generator[None, None, None]:
    """Mask existing creds in environment - used on all tests"""
    # Overrides existing values from conftest.py
    with patch.dict(os.environ, MOCK_TOKENS):
        yield None


@pytest.mark.parametrize(
    ("pop_key"),
    ("TW_CONSUMER_KEY", "TW_CONSUMER_SECRET", "TW_ACCESS_TOKEN", "TW_ACCESS_SECRET"),
)
def test_initialization_raises_error_if_env_vars_missing(pop_key: str) -> None:
    with patch.dict(os.environ):
        os.environ.pop(pop_key)
        with pytest.raises(ValueError):
            UserTUIAuthClient()


def test_key_collect() -> None:
    client = UserTUIAuthClient()
    assert client._generate_oauth_keys()


def test_generate_paramter_string() -> None:
    client = UserTUIAuthClient()
    with patch.dict(os.environ, MOCK_TOKENS):
        keys = client._generate_oauth_keys()
        keys["oauth_nonce"] = MOCK_VALUES["oauth_nonce"]
        keys["oauth_timestamp"] = MOCK_VALUES["oauth_timestamp"]
        parameter_string = client._generate_parameter_string(
            keys, MOCK_VALUES["fields"]
        )
    assert parameter_string == MOCK_VALUES["expected_parameter_string"]


def test_generate_signature_base_string() -> None:
    client = UserTUIAuthClient()
    parameter_string = MOCK_VALUES["expected_parameter_string"]
    base_string = client._generate_base_string(
        method=MOCK_VALUES["method"],
        route=MOCK_VALUES["route"],
        parameter_string=parameter_string,
    )
    assert base_string == MOCK_VALUES["expected_base_string"]


def test_generate_signature_string() -> None:
    client = UserTUIAuthClient()
    base_string = MOCK_VALUES["expected_base_string"]
    with patch.dict(os.environ, MOCK_TOKENS):
        signature = client._generate_signature_string(base_string)
    assert signature == MOCK_VALUES["expected_signature"]


def test_generate_oauth_header() -> None:
    client = UserTUIAuthClient()
    header = client._generate_oauth_header(MOCK_HEADER_VALUES)
    assert header == MOCK_VALUES["expected_header"]


def test_user_authentication_request_fails() -> None:
    client = UserTUIAuthClient()
    with patch.object(client, "_request_user_permission") as user_perm:
        user_perm.return_value = None
        assert client.authenticate() is False
        user_perm.reset_mock()


def test_user_authentication_validation_fails() -> None:
    client = UserTUIAuthClient()
    with patch.object(client, "_request_user_permission") as user_perm:
        user_perm.return_value = MOCK_RESPONSE
        with patch("builtins.input", lambda user_in: "PIN"):
            with patch.object(client, "_validate_authentication") as validate:
                validate.return_value = None
                assert client.authenticate() is False
                assert user_perm.call_count == 1
                assert validate.call_count == 1
                validate.assert_called_with(MOCK_RESPONSE.oauth_token, "PIN")


def test_user_authentication_success() -> None:
    client = UserTUIAuthClient()
    with patch.object(client, "_request_user_permission") as user_perm:
        user_perm.return_value = MOCK_RESPONSE
        with patch("builtins.input", lambda user_in: "PIN"):
            with patch.object(client, "_validate_authentication") as validate:
                validate.return_value = MOCK_RESPONSE
                assert client.authenticate() is True
                assert user_perm.call_count == 1
                assert validate.call_count == 1
                validate.assert_called_with(MOCK_RESPONSE.oauth_token, "PIN")


def test_request_user_permission_success() -> None:
    client = UserTUIAuthClient()
    request = MagicMock(return_value=MagicMock(status_code=200, text=USER_RESP))
    with patch.object(client.http, "post", request):
        result = client._request_user_permission()
        assert isinstance(result, UserOAuthResponse)


def test_request_user_permission_failure() -> None:
    client = UserTUIAuthClient()
    request = MagicMock(return_value=MagicMock(status_code=401, text="errors"))
    with patch.object(client.http, "post", request):
        result = client._request_user_permission()
        assert result is None


def test_validate_authentication_success() -> None:
    client = UserTUIAuthClient()
    request = MagicMock(return_value=MagicMock(status_code=200, text=USER_RESP))
    with patch.object(client.http, "post", request):
        result = client._validate_authentication("mock", "mock")
        assert isinstance(result, UserOAuthResponse)


def test_validate_authentication_failure() -> None:
    client = UserTUIAuthClient()
    request = MagicMock(return_value=MagicMock(data=b"errors"))
    with patch.object(client.http, "post", request):
        result = client._validate_authentication("mock", "mock")
        assert result is None
