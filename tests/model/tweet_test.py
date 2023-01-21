from __future__ import annotations

import pytest
from twitterapiv2.model.tweet import Tweet


def test_text_too_long() -> None:
    tweet = Tweet()

    with pytest.raises(ValueError, match="Tweet text too long"):
        tweet.text("a" * 281)


def test_text_truncate() -> None:
    tweet = Tweet(auto_truncate=True)

    tweet.text("a" * 281)

    assert tweet.data["text"] == "a" * 280


def test_reply_settings() -> None:
    tweet = Tweet()

    tweet.reply_settings("everyone")

    assert tweet.data["reply_settings"] == "everyone"


def test_reply_settings_invalid() -> None:
    tweet = Tweet()

    with pytest.raises(ValueError, match="Invalid reply_settings"):
        tweet.reply_settings("invalid")


def test_chain() -> None:
    tweet = Tweet()

    tweet.text("Hello, world!").reply_settings("everyone")

    assert tweet.data["text"] == "Hello, world!"
    assert tweet.data["reply_settings"] == "everyone"


def test_poll_invalid_option_length() -> None:
    tweet = Tweet()

    with pytest.raises(ValueError, match="Poll option"):
        tweet.poll(["a", "b", "a" * 26], 1)


def test_poll_valid_option_length() -> None:
    tweet = Tweet()

    tweet.poll(["a", "b", "a" * 25], 1)

    assert tweet.data["poll"] == {
        "options": ["a", "b", "a" * 25],
        "duration_minutes": 1,
    }


def test_poll_auto_truncate() -> None:
    tweet = Tweet(auto_truncate=True)

    tweet.poll(["a" * 26, "a" * 25], 1)

    assert tweet.data["poll"] == {
        "options": ["a" * 25, "a" * 25],
        "duration_minutes": 1,
    }


def test_poll_invalid_options() -> None:
    tweet = Tweet()

    with pytest.raises(ValueError, match="Invalid number of options"):
        tweet.poll(["Yes"], 1)

    with pytest.raises(ValueError, match="Invalid number of options"):
        tweet.poll(["Yes", "No", "Maybe", "I don't know", "Yes"], 1)


def test_poll_invalid_duration() -> None:
    tweet = Tweet()

    with pytest.raises(ValueError, match="Invalid duration"):
        tweet.poll(["Yes", "No"], 0)
    with pytest.raises(ValueError, match="Invalid duration"):
        tweet.poll(["Yes", "No"], 10081)


def test_direct_message_deep_link() -> None:
    link = "https://twitter.com/messages/1234567890"
    tweet = Tweet()

    tweet.direct_message_deep_link(link)

    assert tweet.data["direct_message_deep_link"] == link


def test_for_super_followers_only() -> None:
    tweet = Tweet()

    tweet.for_super_followers_only()

    assert tweet.data["for_super_followers_only"] is True


def test_geo() -> None:
    tweet = Tweet()

    tweet.geo("5a110d312052166f")

    assert tweet.data["geo"]["place_id"] == "5a110d312052166f"


def test_media() -> None:
    tweet = Tweet()

    tweet.media(["1234567890"], ["1234567890"])

    assert tweet.data["media"]["media_ids"] == ["1234567890"]
    assert tweet.data["media"]["tagged_user_ids"] == ["1234567890"]


def test_media_no_tagged_users() -> None:
    tweet = Tweet()

    tweet.media(["1234567890"])

    assert tweet.data["media"]["media_ids"] == ["1234567890"]
    assert "tagged_user_ids" not in tweet.data["media"]


def test_quoted_tweet_id() -> None:
    tweet = Tweet()

    tweet.quoted_tweet_id("1234567890")

    assert tweet.data["quoted_tweet_id"] == "1234567890"


def test_reply_with_exclude_reply_user_ids() -> None:
    tweet = Tweet()

    tweet.reply("1234567890", ["1234567890"])

    assert tweet.data["reply"]["in_reply_to_tweet_id"] == "1234567890"
    assert tweet.data["reply"]["exclude_reply_user_ids"] == ["1234567890"]


def test_reply_no_exclude_reply_user_ids() -> None:
    tweet = Tweet()

    tweet.reply("1234567890")

    assert tweet.data["reply"]["in_reply_to_tweet_id"] == "1234567890"
    assert "exclude_reply_user_ids" not in tweet.data["reply"]
