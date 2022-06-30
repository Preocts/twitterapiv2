from __future__ import annotations

from typing import Generator
from unittest.mock import patch

import pytest
from http_overeasy.client_mocker import ClientMocker
from twitterapiv2.model.recent.data import Data
from twitterapiv2.tweets_lookup import TweetsLookup
from twitterapiv2.tweets_lookup import URL

from tests.fixtures.mock_headers import HEADERS

LUCKY_ID = "1461880347478528007"
LUCKY_IDS = "1461880347478528007, 1461880346580979715"

SINGLE_SEARCH = b'{"data":[{"id":"1461880347478528007","text":"Can you please play?"}]}'
MULTI_SEARCH = b'{"data":[{"id":"1461880347478528007","text":"RT Hello"},{"id":"1461880346580979715","text":"RT Hello"}]}'  # noqa: E501


@pytest.fixture
def client() -> Generator[TweetsLookup, None, None]:
    tweetclient = TweetsLookup()
    with patch.object(tweetclient, "http", ClientMocker()):
        yield tweetclient


def test_valid_single_search(client: TweetsLookup) -> None:
    client.http.add_response(SINGLE_SEARCH, HEADERS, 200, URL)

    client.ids(LUCKY_ID)
    result = client.fetch()
    assert len(result) == 1
    assert isinstance(result[0], Data)


def test_valid_multi_search(client: TweetsLookup) -> None:
    client.http.add_response(MULTI_SEARCH, HEADERS, 200, URL)

    client.ids(LUCKY_IDS)
    result = client.fetch()
    assert len(result) == 2


def test_id_required() -> None:
    client = TweetsLookup()
    with pytest.raises(ValueError):
        client.fetch()
