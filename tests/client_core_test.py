from __future__ import annotations

import json
from datetime import datetime
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from httpx import Response
from twitterapiv2.client_core import ClientCore
from twitterapiv2.exceptions import InvalidResponseError
from twitterapiv2.exceptions import ThrottledError
from twitterapiv2.model.application_auth import ApplicationAuth
from twitterapiv2.model.client_auth import ClientAuth

BODY = b'{"data":[{"id":"1461880347478528007","text":"MOCK"}]}'
HEADERS = {
    "api-version": "2.30",
    "cache-control": "no-cache, no-store, max-age=0",
    "content-disposition": " attachment; filename=json.json",
    "content-length": "248",
    "content-type": "application/json; charset=utf-8",
    "date": "Fri, 26 Nov 2021 09:04:24 UTC",
    "server": "tsa_b",
    "set-cookie": "",
    "strict-transport-security": "max-age=631138519",
    "x-access-level": "read",
    "x-connection-hash": "025826e4ff9a90bd701f81d6380501dd64c46f17c69ca21dec15a7c52",
    "x-content-type-options": "nosniff",
    "x-frame-options": "SAMEORIGIN",
    "x-rate-limit-limit": "300",
    "x-rate-limit-remaining": "297",
    "x-rate-limit-reset": "1637917876",
    "x-response-time": "62",
    "x-xss-protection": "0",
}

MOCK_RESPONSE = Response(200, content=BODY, headers=HEADERS)


@pytest.fixture
def client() -> ClientCore:
    auth_mock = MagicMock(get_consumer_bearer=MagicMock(return_value="mock_bearer"))
    return ClientCore(auth_mock)


def test_factory_client_auth() -> None:
    model = ClientAuth("mock", "mock", "https://mock")

    result = ClientCore.from_model(model)

    assert result


def test_factory_app_auth() -> None:
    model = ApplicationAuth("mock", "mock", "mock")

    result = ClientCore.from_model(model)

    assert result


def test_factory_raises_on_unknown() -> None:
    with pytest.raises(ValueError):
        ClientCore.from_model("Something")  # type: ignore


def test_default_values(client: ClientCore) -> None:
    assert client.limit_remaining == -1
    assert client.limit_reset is not None


def test_properties(client: ClientCore) -> None:
    expected_remaining = MOCK_RESPONSE.headers["x-rate-limit-remaining"]
    reset = MOCK_RESPONSE.headers["x-rate-limit-reset"]
    expected_reset = datetime.utcfromtimestamp(int(reset))
    client._last_response = MOCK_RESPONSE

    assert client.limit_remaining == int(expected_remaining)
    assert client.limit_reset == expected_reset


def test_more(client: ClientCore) -> None:
    assert not client.more
    client._next_token = "not null"
    assert client.more


def test_fields(client: ClientCore) -> None:
    assert not len(client.fields)

    client.field_builder._fields = {
        "Valid": "Hello",
        "Invalid": None,
    }

    assert "Valid" in client.fields
    assert "Invalid" not in client.fields


def test_response_handling_429(client: ClientCore) -> None:
    mock_resp = Response(429, headers=HEADERS)
    with pytest.raises(ThrottledError):
        client.raise_on_response("https://", mock_resp)


def test_response_handling_401(client: ClientCore) -> None:
    mock_resp = Response(401, headers=HEADERS)
    with pytest.raises(InvalidResponseError):
        client.raise_on_response("https://", mock_resp)


def test_response_handling_invalid(client: ClientCore) -> None:
    mock_resp = Response(42, headers=HEADERS)
    with pytest.raises(InvalidResponseError):
        client.raise_on_response("https://", mock_resp)


def test_response_handing_200(client: ClientCore) -> None:
    mock_resp = Response(200, headers=HEADERS)
    client.raise_on_response("https://", mock_resp)


def test_get(client: ClientCore) -> None:
    client._last_response = MOCK_RESPONSE
    client.field_builder._fields = {"fields": "mock"}

    with patch.object(client.http, "get", return_value=MOCK_RESPONSE) as mock_get:
        result = client.get("https://mock")

        assert result
        assert client._next_token is None
        assert client._last_response == MOCK_RESPONSE
        mock_get.assert_called_once_with(
            url="https://mock",
            params={"fields": "mock"},
            headers=client.headers,
        )


def test_post(client: ClientCore) -> None:
    client._last_response = MOCK_RESPONSE

    with patch.object(client.http, "post", return_value=MOCK_RESPONSE) as mock_post:
        result = client.post("https://mock", json={"payload": "mock"})

        assert result
        assert client._next_token is None
        assert client._last_response == MOCK_RESPONSE
        mock_post.assert_called_once_with(
            url="https://mock",
            headers=client.headers,
            json={"payload": "mock"},
        )


def test_delete(client: ClientCore) -> None:
    client._last_response = MOCK_RESPONSE

    with patch.object(client.http, "delete", return_value=MOCK_RESPONSE) as mock_delete:
        result = client.unlike("https://mock")

        assert result
        assert client._next_token is None
        assert client._last_response == MOCK_RESPONSE
        mock_delete.assert_called_once_with(
            url="https://mock",
            headers=client.headers,
        )


def test_me(client: ClientCore) -> None:
    mock_resp_body = {
        "data": {
            "id": "mock_id",
            "name": "mock_name",
            "username": "mock_username",
        },
    }
    mock_resp = Response(200, content=json.dumps(mock_resp_body), headers=HEADERS)

    with patch.object(client, "get", return_value=mock_resp):
        result = client.get_user()

        assert result.id == "mock_id"
        assert result.name == "mock_name"
        assert result.username == "mock_username"
