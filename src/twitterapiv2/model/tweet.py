"""
Data model for a Tweet

https://developer.twitter.com/en/docs/twitter-api/tweets/manage-tweets/api-reference/post-tweets
"""
from __future__ import annotations

from typing import Any

VALID_REPLY_SETTINGS = ["everyone", "mentioned_users", "none"]
MIN_POLL_DURATION = 1
MAX_POLL_DURATION = 10080
MIN_POLL_OPTIONS = 2
MAX_POLL_OPTIONS = 4
MAX_POLL_OPTION_LENGTH = 25
MAX_TWEET_LENGTH = 280


class Tweet:
    """Data model for a Tweet"""

    def __init__(self, *, auto_truncate: bool = False) -> None:
        """
        Create an empty Tweet object.

        Keyword Args:
            auto_truncate: Automatically truncate text to fit within limits

        Raises:
            ValueError: If auto_truncate is False and text is too long
        """
        self._auto_truncate = auto_truncate
        self._data: dict[str, Any] = {
            "text": None,
            "reply_settings": None,
            "poll": None,
            "direct_message_deep_link": None,
        }

    @property
    def data(self) -> dict[str, Any]:
        """Return the data of the Tweet"""
        return self._data

    def text(self, text: str) -> Tweet:
        """Set the text of the Tweet"""
        if not self._auto_truncate and len(text) > MAX_TWEET_LENGTH:
            raise ValueError(f"Tweet text too long: {len(text)}")
        self._data["text"] = text[:MAX_TWEET_LENGTH]
        return self

    def reply_settings(self, reply_settings: str) -> Tweet:
        """
        Set the reply settings of the Tweet

        Valid values are:
        - everyone
        - mentioned_users
        - none
        """
        if reply_settings not in VALID_REPLY_SETTINGS:
            raise ValueError(f"Invalid reply_settings: {reply_settings}")
        self._data["reply_settings"] = reply_settings
        return self

    def poll(self, options: list[str], duration_minutes: int) -> Tweet:
        """
        Set the poll of the Tweet

        Args:
            options: List of options for the poll (max 4) (max 25 characters per option)
            duration_minutes: Duration of the poll in minutes (max 10080 minutes)
        """
        if len(options) > MAX_POLL_OPTIONS or len(options) < MIN_POLL_OPTIONS:
            raise ValueError(f"Invalid number of options: {len(options)}")
        if duration_minutes > MAX_POLL_DURATION or duration_minutes < MIN_POLL_DURATION:
            raise ValueError(f"Invalid duration: {duration_minutes}")
        if not self._auto_truncate:
            for option in options:
                if len(option) > MAX_POLL_OPTION_LENGTH:
                    raise ValueError(f"Poll option '{option}' too long: {len(option)}")

        options_trimmed = [option[:MAX_POLL_OPTION_LENGTH] for option in options]
        self._data["poll"] = {
            "options": options_trimmed,
            "duration_minutes": duration_minutes,
        }
        return self

    def direct_message_deep_link(self, direct_message_deep_link: str) -> Tweet:
        """Set the direct message deep link of the Tweet"""
        self._data["direct_message_deep_link"] = direct_message_deep_link
        return self
