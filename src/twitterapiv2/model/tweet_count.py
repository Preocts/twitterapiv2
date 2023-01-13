from __future__ import annotations

from typing import TypedDict


class Meta(TypedDict, total=False):
    total_tweet_count: int
    next_token: str


class TweetCount(TypedDict, total=False):
    start: str
    end: str
    tweet_count: int
    meta: Meta
