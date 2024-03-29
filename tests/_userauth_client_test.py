from __future__ import annotations

from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from twitterapiv2._userauth_client import TWITTER_AUTH
from twitterapiv2._userauth_client import TWITTER_TOKEN
from twitterapiv2._userauth_client import UserAuthClient
from twitterapiv2.model.client_auth import ClientAuth


@pytest.fixture
def client() -> UserAuthClient:
    return UserAuthClient(MagicMock(), [])


def test__code_verifier(client: UserAuthClient) -> None:
    result = client._code_verifier()

    assert isinstance(result, str)


def test__code_challenge(client: UserAuthClient) -> None:
    verifier = "happy go lucky"
    expected = "F9i_m3bYeE8Wrw_rHubiV4coAXzx9eDbRxK_1dVnfX0"
    result = client._code_challenge(verifier)

    assert result == expected


def test__get_bearer_token(client: UserAuthClient) -> None:
    with patch.object(client, "_oauth2_client") as mock_oauth2:
        mock_oauth2.return_value.create_authorization_url.return_value = (
            "https://mock.auth.url",
            None,
        )
        mock_oauth2.return_value.fetch_token.return_value = {"access_token": "mock"}

        with patch.object(client, "_get_authorization_response") as mock_response:
            with patch.object(client, "_code_verifier", return_value="verifier"):
                mock_response.return_value = "mock_response"

                result = client.get_bearer()

                assert result == "mock"
                mock_oauth2().create_authorization_url.assert_called_once_with(
                    url=TWITTER_AUTH,
                    code_verifier="verifier",
                    code_challenge=client._code_challenge("verifier"),
                    code_challenge_method="S256",
                )

                mock_oauth2().fetch_token.assert_called_once_with(
                    url=TWITTER_TOKEN,
                    grant_type="authorization_code",
                    authorization_response="mock_response",
                    code_verifier="verifier",
                )


def test__get_bearer_token_exists(client: UserAuthClient) -> None:
    client._bearer = "mock_bearer"

    with patch.object(client, "_oauth2_client") as mock_oauth2:
        with patch.object(client, "_get_authorization_response"):
            result = client.get_bearer()

            assert result == "mock_bearer"
            mock_oauth2().create_authorization_url.assert_not_called()
            mock_oauth2().fetch_token.assert_not_called()


def test__oauth2_client(client: UserAuthClient) -> None:
    client._keys = ClientAuth("mock_id", "mock_secret", "127.0.0.1")

    result = client._oauth2_client()

    assert result.client_id == "mock_id"
    assert result.client_secret == "mock_secret"
    assert result.redirect_uri == "127.0.0.1"
    assert result.scope == []


def test__get_authorization_response(client: UserAuthClient) -> None:
    with patch("builtins.input") as mock_input:
        mock_input.return_value = "groovy"

        assert client._get_authorization_response("Some String") == "groovy"
