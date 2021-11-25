from datetime import datetime

import pytest
from twitterapiv2.client_intrfc import ClientIntrfc
from twitterapiv2.model.responseheader import ResponseHeader

MOCK_LAST_RESPONSE = ResponseHeader()


def test_default_values() -> None:
    client = ClientIntrfc()
    assert client.limit_remaining == -1
    assert client.limit_reset is not None


def test_properties() -> None:
    client = ClientIntrfc()
    reset = datetime.utcfromtimestamp(1637818406)
    mock_response = ResponseHeader()
    mock_response.x_rate_limit_remaining = "10"
    mock_response.x_rate_limit_reset = "1637818406"

    client.http.last_response = mock_response

    assert client.limit_remaining == 10
    assert client.limit_reset == reset


def test_more() -> None:
    client = ClientIntrfc()
    assert not client.more
    client._next_token = "not null"
    assert client.more


def test_fields() -> None:
    client = ClientIntrfc()
    assert not len(client.fields)

    client.field_builder._fields = {
        "Valid": "Hello",
        "Invalid": None,
    }

    assert "Valid" in client.fields
    assert "Invalid" not in client.fields


def test_fetch_not_implemented() -> None:
    client = ClientIntrfc()
    with pytest.raises(NotImplementedError):
        client.fetch()
