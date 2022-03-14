import json

import pytest
from twitterapiv2.model.response import Response
from urllib3.response import HTTPResponse

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

MOCK_RESPONSE = HTTPResponse(body=BODY, headers=HEADERS, status=200)


@pytest.fixture
def mock_resp() -> None:
    return Response(MOCK_RESPONSE)


def test_status(mock_resp: Response) -> None:
    assert mock_resp.get_status() == 200


def test_success(mock_resp: Response) -> None:
    assert mock_resp.has_success() is True


def test_headers(mock_resp: Response) -> None:
    for key, value in HEADERS.items():
        attr = key.replace("-", "_")
        assert getattr(mock_resp.get_headers(), attr) == value


def test_body(mock_resp: Response) -> None:
    assert mock_resp.get_body() == BODY.decode()


def test_json(mock_resp: Response) -> None:
    assert mock_resp.get_json() == json.loads(BODY)


def test_json_invalid(mock_resp: Response) -> None:
    mock_resp._body = b""

    assert mock_resp.get_json() is None
