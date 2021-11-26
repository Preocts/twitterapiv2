from datetime import datetime

import pytest
from twitterapiv2.fields import Fields


def test_builder_start_time() -> None:
    str_time = "2020-10-10T00:00:00Z"
    date_time = datetime.utcnow()
    client = Fields()
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
    client = Fields()
    with pytest.raises(ValueError):
        client.end_time("invalid")
    client.end_time(date_time)

    client = Fields()
    client.end_time(str_time)
    assert client.fields["end_time"] == str_time

    client.end_time(None)
    assert client.fields.get("end_time") is None


def test_builder_since_id() -> None:
    client = Fields()
    client.since_id("1234")
    assert client.fields["since_id"] == "1234"

    client.since_id(None)
    assert client.fields.get("since_id") is None


def test_builder_until_id() -> None:
    client = Fields()
    client.until_id("1234")
    assert client.fields["until_id"] == "1234"

    client.until_id(None)
    assert client.fields.get("until_id") is None


def test_builder_expansions() -> None:
    client = Fields()
    client.expansions("1234")
    assert client.fields["expansions"] == "1234"

    client.expansions(None)
    assert client.fields.get("expansions") is None


def test_builder_media_fields() -> None:
    client = Fields()
    client.media_fields("1234")
    assert client.fields["media.fields"] == "1234"

    client.media_fields(None)
    assert client.fields.get("media.fields") is None


def test_builder_place_fields() -> None:
    client = Fields()
    client.place_fields("1234")
    assert client.fields["place.fields"] == "1234"

    client.place_fields(None)
    assert client.fields.get("place.fields") is None


def test_builder_poll_fields() -> None:
    client = Fields()
    client.poll_fields("1234")
    assert client.fields["poll.fields"] == "1234"

    client.poll_fields(None)
    assert client.fields.get("poll.fields") is None


def test_builder_tweet_fields() -> None:
    client = Fields()
    client.tweet_fields("1234")
    assert client.fields["tweet.fields"] == "1234"

    client.tweet_fields(None)
    assert client.fields.get("tweet.fields") is None


def test_builder_user_fields() -> None:
    client = Fields()
    client.user_fields("1234")
    assert client.fields["user.fields"] == "1234"

    client.user_fields(None)
    assert client.fields.get("user.fields") is None


def test_builder_max_results() -> None:
    client = Fields()
    client.max_results(12)
    assert client.fields["max_results"] == 12

    client.max_results(None)
    assert client.fields.get("max_results") is None

    with pytest.raises(ValueError):
        Fields().max_results(1)

    with pytest.raises(ValueError):
        Fields().max_results(101)


def test_builder_granularity() -> None:
    client = Fields()
    client.granularity("hour")
    assert client.fields["granularity"] == "hour"

    client.granularity(None)
    assert client.fields.get("granularity") is None


def test_builder_id() -> None:
    too_many = ",".join(list("a" * 101))
    client = Fields()
    client.id("123")
    assert client.fields["id"] == "123"

    client.id("123, 348             ")
    assert client.fields["id"] == "123,348"

    with pytest.raises(ValueError):
        client.id(too_many)
