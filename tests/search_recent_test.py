from datetime import datetime

import pytest
import vcr
from twitterapiv2.model.recent.recent import Recent
from twitterapiv2.search_recent import SearchRecent

api_recorder = vcr.VCR(
    filter_headers=["Authorization"],
    record_mode="ONCE",
    cassette_library_dir="tests/cassettes/search_recent",
)


@api_recorder.use_cassette()
def test_valid_search() -> None:
    # NOTE: To re-record this test a valid bearer token must be
    # injected into the env. Use the confest autouse fixture.
    client = SearchRecent().max_results(10)

    result = client.search("hello")
    assert isinstance(result, Recent)
    assert result.data
    next_token = client.next_token
    assert next_token

    result = client.search("hello", page_token=next_token)
    assert client.next_token != next_token


def test_builder_start_time() -> None:
    str_time = "2020-10-10T00:00:00Z"
    date_time = datetime.utcnow()
    with pytest.raises(ValueError):
        SearchRecent().start_time("invalid")
    SearchRecent().start_time(date_time)
    client = SearchRecent().start_time(str_time)
    assert client.fields["start_time"] == str_time


def test_builder_end_time() -> None:
    str_time = "2020-10-10T00:00:00Z"
    date_time = datetime.utcnow()
    with pytest.raises(ValueError):
        SearchRecent().end_time("invalid")
    SearchRecent().end_time(date_time)
    client = SearchRecent().end_time(str_time)
    assert client.fields["end_time"] == str_time


def test_builder_since_id() -> None:
    client = SearchRecent().since_id("1234")
    assert client.fields["since_id"] == "1234"


def test_builder_until_id() -> None:
    client = SearchRecent().until_id("1234")
    assert client.fields["until_id"] == "1234"


def test_builder_expansions() -> None:
    client = SearchRecent().expansions("1234")
    assert client.fields["expansions"] == "1234"


def test_builder_media_fields() -> None:
    client = SearchRecent().media_fields("1234")
    assert client.fields["media.fields"] == "1234"


def test_builder_place_fields() -> None:
    client = SearchRecent().place_fields("1234")
    assert client.fields["place.fields"] == "1234"


def test_builder_poll_fields() -> None:
    client = SearchRecent().poll_fields("1234")
    assert client.fields["poll.fields"] == "1234"


def test_builder_tweet_fields() -> None:
    client = SearchRecent().tweet_fields("1234")
    assert client.fields["tweet.fields"] == "1234"


def test_builder_user_fields() -> None:
    client = SearchRecent().user_fields("1234")
    assert client.fields["user.fields"] == "1234"


def test_builder_max_results() -> None:
    client = SearchRecent().max_results(12)
    assert client.fields["max_results"] == "12"

    with pytest.raises(ValueError):
        SearchRecent().max_results(1)

    with pytest.raises(ValueError):
        SearchRecent().max_results(101)
