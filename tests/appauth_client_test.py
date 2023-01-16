from __future__ import annotations

from unittest.mock import patch

import pytest
from twitterapiv2.appauth_client import AppAuthClient
from twitterapiv2.model.application_auth import ApplicationAuth

from tests.fixtures.httpmocker import HttpMocker

MOCK_KEY = "xvz1evFS4wEEPTGEFPHBog"
MOCK_SECRET = "L8qq9PZyRg6ieKGEKhZolGC0vJWLw8iEJ88DRdyOg"
MOCK_CRED = "eHZ6MWV2RlM0d0VFUFRHRUZQSEJvZzpMOHFxOVBaeVJnNmllS0dFS2hab2xHQzB2SldMdzhpRUo4OERSZHlPZw=="  # noqa: E501
MOCK_BEARER = "AAAAAAAAAAAAAAAAAAAAAP84VgEAAAAAQY8EsmI4GGhUif1WbMYnbLfrOyA%3DOY35WqNFisAnDtjp08qaXjYB2n6xncWp3pdoAOPPjx6gUL2Y83"  # noqa: E501

MOCK_RESP = '{"token_type":"bearer","access_token":"AAAAAAAAAAAAAAAAAAAAAP84VgEAAAAAQY8EsmI4GGhUif1WbMYnbLfrOyA%3DOY35WqNFisAnDtjp08qaXjYB2n6xncWp3pdoAOPPjx6gUL2Y83"}'  # noqa: E501
BAD_REQUEST = '{"errors":[{"code":99,"message":"Unable to verify your credentials","label":"authenticity_token_error"}]}'  # noqa: 501
BAD_RESPONSE = '{"token_type":"bearer"}'


@pytest.fixture
def client() -> AppAuthClient:
    return AppAuthClient(ApplicationAuth(MOCK_KEY, MOCK_SECRET))


def test_encoded_credentials(client: AppAuthClient) -> None:
    result = client._encoded_credentials()
    assert result == MOCK_CRED


def test_required_applicationauth_key(client: AppAuthClient) -> None:
    client._keys.consumer_key = ""
    with pytest.raises(KeyError):
        client._encoded_credentials()


def test_required_applicationauth_secret(client: AppAuthClient) -> None:
    client._keys.consumer_secret = ""
    with pytest.raises(KeyError):
        client._encoded_credentials()


def test_get_consumer_bearer(client: AppAuthClient) -> None:
    with patch.object(client, "http", HttpMocker()) as mock_http:
        mock_http.add_response(MOCK_RESP, {}, 200, client.twitter_api + "/oauth2/token")

        result = client.get_consumer_bearer()

        assert result == MOCK_BEARER


def test_invalid_bearer_request(client: AppAuthClient) -> None:
    with patch.object(client, "http", HttpMocker()) as mock_http:
        mock_http.add_response(
            BAD_REQUEST, {}, 403, client.twitter_api + "/oauth2/token"
        )

        with pytest.raises(ValueError):
            client._get_bearer_token()


def test_invalid_bearer_response(client: AppAuthClient) -> None:
    with patch.object(client, "http", HttpMocker()) as mock_http:
        mock_http.add_response(
            BAD_RESPONSE, {}, 200, client.twitter_api + "/oauth2/token"
        )

        with pytest.raises(ValueError):
            client._get_bearer_token()


def test_get_consumer_bearer_when_exists(client: AppAuthClient) -> None:
    client._keys.consumer_bearer = "mock"

    result = client.get_consumer_bearer()

    assert result == "mock"


def test_revoke_bearer_token(client: AppAuthClient) -> None:
    client._keys.consumer_bearer = "mock"

    client.revoke_bearer_token()

    assert client._keys.consumer_bearer is None
