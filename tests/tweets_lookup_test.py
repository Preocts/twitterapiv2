from __future__ import annotations

from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from twitterapiv2.tweets_lookup import TweetsLookup
from twitterapiv2.tweets_lookup import URL

from tests.fixtures.httpmocker import HttpMocker
from tests.fixtures.mock_headers import HEADERS

LUCKY_ID = "1461880347478528007"
LUCKY_IDS = "1461880347478528007, 1461880346580979715"

SINGLE_SEARCH = b'{"data":[{"id":"1461880347478528007","text":"Can you please play?"}]}'
MULTI_SEARCH = b'{"data":[{"id":"1461880347478528007","text":"RT Hello"},{"id":"1461880346580979715","text":"RT Hello"}]}'  # noqa: E501


@pytest.fixture
def client() -> TweetsLookup:
    return TweetsLookup(MagicMock())


def test_valid_single_search(client: TweetsLookup) -> None:
    with patch.object(client, "http", HttpMocker()) as mock_http:
        mock_http.add_response(SINGLE_SEARCH, HEADERS, 200, URL)

        client.ids(LUCKY_ID)
        result = client.fetch()
        assert len(result) == 1


def test_valid_multi_search(client: TweetsLookup) -> None:
    with patch.object(client, "http", HttpMocker()) as mock_http:
        mock_http.add_response(MULTI_SEARCH, HEADERS, 200, URL)

        client.ids(LUCKY_IDS)
        result = client.fetch()
        assert len(result) == 2


def test_id_required(client: TweetsLookup) -> None:
    with pytest.raises(ValueError):
        client.fetch()
