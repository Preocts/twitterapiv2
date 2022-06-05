from __future__ import annotations

import re
from typing import NamedTuple

USER_PATTERN = (
    "^oauth_token=(.*?)&oauth_token_secret=(.*?)&oauth_callback_confirmed=true$"
)
ACCESS_PATTERN = (
    "^oauth_token=(.*?)&oauth_token_secret=(.*?)&user_id=([0-9]*)&screen_name=(.*?)$"
)


class UserOAuthResponse(NamedTuple):
    oauth_token: str
    oauth_token_secret: str
    user_id: str | None = None
    screen_name: str | None = None

    @classmethod
    def from_resp_string(cls, response: str) -> UserOAuthResponse:
        """
        Creates object from Twitter response string

        Args
            response: string response from Twitter

        Returns
            UserOAuthResponse

        Raises
            ValueError: on response not matching expected format
        """
        user_match = re.match(USER_PATTERN, response)
        access_match = re.match(ACCESS_PATTERN, response)

        if user_match is not None:
            return cls(
                oauth_token=user_match.group(1),
                oauth_token_secret=user_match.group(2),
            )
        elif access_match is not None:
            return cls(
                oauth_token=access_match.group(1),
                oauth_token_secret=access_match.group(2),
                user_id=access_match.group(3),
                screen_name=access_match.group(4),
            )
        raise ValueError("No match for response string.")
