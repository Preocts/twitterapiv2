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


def test_poll() -> None:
    tweet = Tweet()
    tweet.poll(["Yes", "No"], 1)
    assert tweet.data["poll"] == {"options": ["Yes", "No"], "duration_minutes": 1}


def test_poll_invalid_options() -> None:
    tweet = Tweet()
    with pytest.raises(ValueError):
        tweet.poll(["Yes"], 1)
    with pytest.raises(ValueError):
        tweet.poll(["Yes", "No", "Maybe", "I don't know", "Yes"], 1)


def test_poll_invalid_duration() -> None:
    tweet = Tweet()
    with pytest.raises(ValueError):
        tweet.poll(["Yes", "No"], 0)
    with pytest.raises(ValueError):
        tweet.poll(["Yes", "No"], 10081)


def test_direct_message_deep_link() -> None:
    link = "https://twitter.com/messages/1234567890"
    tweet = Tweet()
    tweet.direct_message_deep_link(link)
    assert tweet.data["direct_message_deep_link"] == link
