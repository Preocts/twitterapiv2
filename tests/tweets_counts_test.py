import pytest
from twitterapiv2.model.tweet_count.tweet_count import TweetCount
from twitterapiv2.tweets_counts import TweetsCounts


def test_valid_count() -> None:
    # NOTE: To re-record this test a valid bearer token must be
    # injected into the env. Use the confest autouse fixture.
    client = TweetsCounts()
    client.query("hello")

    result = client.fetch()
    assert isinstance(result, TweetCount)
    assert result.meta.total_tweet_count
    assert not client.more


def test_query_required() -> None:
    client = TweetsCounts()
    with pytest.raises(ValueError):
        client.fetch()
