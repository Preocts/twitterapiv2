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
    client = SearchRecent()
    client.max_results(10)

    result = client.fetch("hello")
    assert isinstance(result, Recent)
    assert result.data
    next_token = client.next_token
    assert next_token

    result = client.fetch("hello", page_token=next_token)
    assert client.next_token != next_token


def test_builder_start_time() -> None:
    str_time = "2020-10-10T00:00:00Z"
    date_time = datetime.utcnow()
    client = SearchRecent()
    with pytest.raises(ValueError):
        client.start_time("invalid")
    client.start_time(date_time)

    client.start_time(str_time)
    assert client.fields["start_time"] == str_time

    client.start_time(None)
    assert client.fields.get("start_time") is None


def test_builder_end_time() -> None:
    str_time = "2020-10-10T00:00:00Z"
    date_time = datetime.utcnow()
    client = SearchRecent()
    with pytest.raises(ValueError):
        client.end_time("invalid")
    SearchRecent().end_time(date_time)

    client = SearchRecent()
    client.end_time(str_time)
    assert client.fields["end_time"] == str_time

    client.end_time(None)
    assert client.fields.get("end_time") is None


def test_builder_since_id() -> None:
    client = SearchRecent()
    client.since_id("1234")
    assert client.fields["since_id"] == "1234"

    client.since_id(None)
    assert client.fields.get("since_id") is None


def test_builder_until_id() -> None:
    client = SearchRecent()
    client.until_id("1234")
    assert client.fields["until_id"] == "1234"

    client.until_id(None)
    assert client.fields.get("until_id") is None


def test_builder_expansions() -> None:
    client = SearchRecent()
    client.expansions("1234")
    assert client.fields["expansions"] == "1234"

    client.expansions(None)
    assert client.fields.get("expansions") is None


def test_builder_media_fields() -> None:
    client = SearchRecent()
    client.media_fields("1234")
    assert client.fields["media.fields"] == "1234"

    client.media_fields(None)
    assert client.fields.get("media.fields") is None


def test_builder_place_fields() -> None:
    client = SearchRecent()
    client.place_fields("1234")
    assert client.fields["place.fields"] == "1234"

    client.place_fields(None)
    assert client.fields.get("place.fields") is None


def test_builder_poll_fields() -> None:
    client = SearchRecent()
    client.poll_fields("1234")
    assert client.fields["poll.fields"] == "1234"

    client.poll_fields(None)
    assert client.fields.get("poll.fields") is None


def test_builder_tweet_fields() -> None:
    client = SearchRecent()
    client.tweet_fields("1234")
    assert client.fields["tweet.fields"] == "1234"

    client.tweet_fields(None)
    assert client.fields.get("tweet.fields") is None


def test_builder_user_fields() -> None:
    client = SearchRecent()
    client.user_fields("1234")
    assert client.fields["user.fields"] == "1234"

    client.user_fields(None)
    assert client.fields.get("user.fields") is None


def test_builder_max_results() -> None:
    client = SearchRecent()
    client.max_results(12)
    assert client.fields["max_results"] == "12"

    client.max_results(None)
    assert client.fields.get("max_results") is None

    with pytest.raises(ValueError):
        SearchRecent().max_results(1)

    with pytest.raises(ValueError):
        SearchRecent().max_results(101)
