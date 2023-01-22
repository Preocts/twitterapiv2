from __future__ import annotations

from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from twitterapiv2.manage_tweets import ManageTweets
from twitterapiv2.model.tweet import Tweet


@pytest.fixture
def client() -> ManageTweets:
    return ManageTweets(MagicMock())


def test_new_tweet(client: ManageTweets) -> None:
    tweet = client.new_tweet()

    assert tweet.data == {}
    assert tweet._auto_truncate is False
    assert isinstance(tweet, Tweet)


def test_new_tweet_with_auto_truncate(client: ManageTweets) -> None:
    tweet = client.new_tweet(auto_truncate=True)

    assert tweet.data == {}
    assert tweet._auto_truncate is True
    assert isinstance(tweet, Tweet)


def test_send_tweet(client: ManageTweets) -> None:
    tweet = client.new_tweet()
    tweet.text("Hello, world!")

    with patch.object(client, "post") as mock_post:
        client.send_tweet(tweet)

        mock_post.assert_called_once_with(
            "https://api.twitter.com/2/tweets", json={"text": "Hello, world!"}
        )


def test_delete_tweet(client: ManageTweets) -> None:
    with patch.object(client, "delete") as mock_delete:
        client.delete_tweet("12345")

        mock_delete.assert_called_once_with("https://api.twitter.com/2/tweets/12345")
