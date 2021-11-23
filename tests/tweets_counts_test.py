from datetime import datetime

import pytest
import vcr
from twitterapiv2.model.tweet_count.tweet_count import TweetCount
from twitterapiv2.tweets_counts import TweetsCounts

api_recorder = vcr.VCR(
    filter_headers=["Authorization"],
    record_mode="ONCE",
    cassette_library_dir="tests/cassettes/tweets_counts",
)


@api_recorder.use_cassette()
def test_valid_count() -> None:
    # NOTE: To re-record this test a valid bearer token must be
    # injected into the env. Use the confest autouse fixture.
    client = TweetsCounts()

    result = client.fetch("hello")
    assert isinstance(result, TweetCount)
    assert result.meta.total_tweet_count
    assert not client.next_token


def test_builder_start_time() -> None:
    str_time = "2020-10-10T00:00:00Z"
    date_time = datetime.utcnow()
    with pytest.raises(ValueError):
        TweetsCounts().start_time("invalid")
    TweetsCounts().start_time(date_time)

    client = TweetsCounts().start_time(str_time)
    assert client.fields["start_time"] == str_time

    client = client.start_time(None)
    assert client.fields.get("start_time") is None


def test_builder_end_time() -> None:
    str_time = "2020-10-10T00:00:00Z"
    date_time = datetime.utcnow()
    with pytest.raises(ValueError):
        TweetsCounts().end_time("invalid")
    TweetsCounts().end_time(date_time)

    client = TweetsCounts().end_time(str_time)
    assert client.fields["end_time"] == str_time

    client = client.end_time(None)
    assert client.fields.get("end_time") is None


def test_builder_since_id() -> None:
    client = TweetsCounts().since_id("1234")
    assert client.fields["since_id"] == "1234"

    client = client.since_id(None)
    assert client.fields.get("since_id") is None


def test_builder_until_id() -> None:
    client = TweetsCounts().until_id("1234")
    assert client.fields["until_id"] == "1234"

    client = client.until_id(None)
    assert client.fields.get("until_id") is None


def test_builder_expansions() -> None:
    client = TweetsCounts().granularity("hour")
    assert client.fields["granularity"] == "hour"

    client = client.granularity(None)
    assert client.fields.get("granularity") is None
