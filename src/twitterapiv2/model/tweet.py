"""
Data model for a Tweet

https://developer.twitter.com/en/docs/twitter-api/tweets/manage-tweets/api-reference/post-tweets
"""
from __future__ import annotations

from typing import Any

VALID_REPLY_SETTINGS = ["everyone", "mentioned_users", "none"]


class Tweet:
    """Data model for a Tweet"""

    def __init__(self) -> None:
        """Create an empty Tweet object"""
        self._data: dict[str, Any] = {
            "text": None,
            "reply_settings": None,
            "poll": None,
        }

    @property
    def data(self) -> dict[str, Any]:
        """Return the data of the Tweet"""
        return self._data

    def text(self, text: str) -> Tweet:
        """Set the text of the Tweet"""
        self._data["text"] = text
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
        if len(options) > 4:
            raise ValueError(f"Too many options: {len(options)}")
        if len(options) < 2:
            raise ValueError(f"Too few options: {len(options)}")
        if duration_minutes > 10080:
            raise ValueError(f"Duration too long: {duration_minutes}")
        if duration_minutes < 1:
            raise ValueError(f"Duration too short: {duration_minutes}")
        options_trimmed = [option[:25] for option in options]
        self._data["poll"] = {
            "options": options_trimmed,
            "duration_minutes": duration_minutes,
        }
        return self
