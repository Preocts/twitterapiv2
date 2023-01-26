from __future__ import annotations

from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from twitterapiv2.likes import Likes

MOCK_USERID = "12345"


@pytest.fixture
def client() -> Likes:
    client_ = Likes(MagicMock())
    client_.get_user = MagicMock(return_value=MagicMock(id=MOCK_USERID))  # type: ignore
    return client_


def test_user_id(client: Likes) -> None:
    result = client.user_id

    assert result == MOCK_USERID
    assert client.user_id is result


def test_get_likes(client: Likes) -> None:
    with patch.object(client, "get") as mock_get:
        client.get_likes()

        mock_get.assert_called_once_with(
            f"https://api.twitter.com/2/users/{MOCK_USERID}/liked_tweets"
        )


def test_unlike(client: Likes) -> None:
    with patch.object(client, "delete") as mock_delete:
        client.unlike("12345")

        mock_delete.assert_called_once_with(
            f"https://api.twitter.com/2/users/{MOCK_USERID}/likes/12345"
        )


def test_like(client: Likes) -> None:
    with patch.object(client, "post") as mock_post:
        client.like("12345")

        mock_post.assert_called_once_with(
            f"https://api.twitter.com/2/users/{MOCK_USERID}/likes",
            {"tweet_id": "12345"},
        )


def test_get_liking_users(client: Likes) -> None:
    with patch.object(client, "get") as mock_get:
        client.get_liking_users("12345")

        mock_get.assert_called_once_with(
            "https://api.twitter.com/2/tweets/12345/liking_users"
        )
