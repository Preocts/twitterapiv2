from __future__ import annotations

import pytest
from twitterapiv2.model.tweet import Tweet


def test_text() -> None:
    tweet = Tweet()
    tweet.text("Hello, world!")
    assert tweet.data["text"] == "Hello, world!"


def test_reply_settings() -> None:
    tweet = Tweet()
    tweet.reply_settings("everyone")
    assert tweet.data["reply_settings"] == "everyone"


def test_reply_settings_invalid() -> None:
    tweet = Tweet()
    with pytest.raises(ValueError):
        tweet.reply_settings("invalid")


def test_chain() -> None:
    tweet = Tweet()
    tweet.text("Hello, world!").reply_settings("everyone")
    assert tweet.data["text"] == "Hello, world!"
    assert tweet.data["reply_settings"] == "everyone"
