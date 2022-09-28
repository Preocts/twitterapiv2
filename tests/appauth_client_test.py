from __future__ import annotations

import os
from typing import Generator
from unittest.mock import patch

import pytest
from twitterapiv2.appauth_client import AppAuthClient

from tests.fixtures.clientmocker import ClientMocker

MOCK_KEY = "xvz1evFS4wEEPTGEFPHBog"
MOCK_SECRET = "L8qq9PZyRg6ieKGEKhZolGC0vJWLw8iEJ88DRdyOg"
MOCK_CRED = "eHZ6MWV2RlM0d0VFUFRHRUZQSEJvZzpMOHFxOVBaeVJnNmllS0dFS2hab2xHQzB2SldMdzhpRUo4OERSZHlPZw=="  # noqa: E501

MOCK_RESP = '{"token_type":"bearer","access_token":"AAAAAAAAAAAAAAAAAAAAAP84VgEAAAAAQY8EsmI4GGhUif1WbMYnbLfrOyA%3DOY35WqNFisAnDtjp08qaXjYB2n6xncWp3pdoAOPPjx6gUL2Y83"}'  # noqa: E501
BAD_REQUEST = '{"errors":[{"code":99,"message":"Unable to verify your credentials","label":"authenticity_token_error"}]}'  # noqa: 501
BAD_RESPONSE = '{"token_type":"bearer"}'


@pytest.fixture
def client() -> Generator[AppAuthClient, None, None]:
    appclient = AppAuthClient()
    with patch.object(appclient, "http", ClientMocker()):
        yield appclient


def test_encoded_credentials() -> None:
    client = AppAuthClient()
    env = {
        "TW_CONSUMER_KEY": MOCK_KEY,
        "TW_CONSUMER_SECRET": MOCK_SECRET,
    }
    with patch.dict(os.environ, env):
        result = client.encoded_credentials()
        assert result == MOCK_CRED


def test_require_environ_vars() -> None:
    client = AppAuthClient()
    os.environ.pop("TW_CONSUMER_KEY", None)
    with pytest.raises(KeyError):
        client.encoded_credentials()

    os.environ["TW_CONSUMER_KEY"] = "Mock"
    os.environ.pop("TW_CONSUMER_SECRET", None)
    with pytest.raises(KeyError):
        client.encoded_credentials()


def test_set_bearer_token(client: AppAuthClient) -> None:
    client.http.add_response(MOCK_RESP, {}, 200, client.twitter_api + "/oauth2/token")

    client.set_bearer_token()

    assert os.getenv("TW_BEARER_TOKEN") is not None


def test_fetch_bearer_token(client: AppAuthClient) -> None:
    client.http.add_response(MOCK_RESP, {}, 200, client.twitter_api + "/oauth2/token")

    client.fetch_bearer_token()

    assert os.getenv("TW_BEARER_TOKEN") is None


def test_invalid_bearer_request(client: AppAuthClient) -> None:
    client.http.add_response(BAD_REQUEST, {}, 403, client.twitter_api + "/oauth2/token")

    with pytest.raises(ValueError):
        client.set_bearer_token()


def test_invalid_bearer_response(client: AppAuthClient) -> None:
    client.http.add_response(
        BAD_RESPONSE, {}, 200, client.twitter_api + "/oauth2/token"
    )

    with pytest.raises(ValueError):
        client.set_bearer_token()
