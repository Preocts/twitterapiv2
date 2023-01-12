"""
https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-recent#Default
"""
from __future__ import annotations

from typing import Any
from typing import TypedDict


class Meta(TypedDict, total=False):
    count: int
    newest_id: int
    oldest_id: int
    next_token: str | None


class Includes(TypedDict, total=False):
    tweets: list[Any]
    users: list[Any]
    places: list[Any]
    media: list[Any]
    polls: str


class PromotedMetrics(TypedDict, total=False):
    impression_count: int
    url_link_click: int
    user_profile_click: int
    retweet_count: int
    reply_count: int
    like_count: int


class OrganicMetrics(TypedDict, total=False):
    impression_count: int
    url_link_click: int
    user_profile_click: int
    retweet_count: int
    reply_count: int
    like_count: int


class NonPublicMetrics(TypedDict, total=False):
    impression_count: int
    url_link_click: int
    user_profile_click: int


class PublicMetrics(TypedDict, total=False):
    retweet_count: int
    reply_count: int
    like_count: int
    quote_count: int


class Withheld(TypedDict, total=False):
    copyright: bool  # noqa: A003
    country_code: list[str]
    scope: int


class Cashtags(TypedDict, total=False):
    start: int
    end: int
    tag: str


class Mentions(TypedDict, total=False):
    start: int
    end: int
    username: str


class Hashtags(TypedDict, total=False):
    start: int
    end: int
    tag: str


class Urls(TypedDict, total=False):
    start: int
    end: int
    url: str
    expanded_url: str
    display_url: str
    unwound_url: str


class Annotations(TypedDict, total=False):
    start: int
    end: int
    probability: float
    type: str  # noqa: A003
    normalized_text: str


class Entities(TypedDict, total=False):
    annotations: list[Annotations]
    urls: list[Urls]
    hashtags: list[Hashtags]
    mentions: list[Mentions]
    cashtags: list[Cashtags]


class Entity(TypedDict, total=False):
    id: str  # noqa: A003
    name: str
    description: str


class Domain(TypedDict, total=False):
    id: str  # noqa: A003
    name: str
    description: str


class ContextAnnotations(TypedDict, total=False):
    domain: Domain
    entity: Entity


class Coordinates(TypedDict, total=False):
    type: str  # noqa: A003
    coordinates: list[float]


class Geo(TypedDict, total=False):
    coordinates: Coordinates
    place_id: str


class Attachments(TypedDict, total=False):
    media_keys: list[str]
    poll_id: list[str]


class ReferencedTweets(TypedDict, total=False):
    id: str  # noqa: A003
    type: int  # noqa: A003


class Data(TypedDict, total=False):
    id: str  # noqa: A003
    text: str
    created_at: str
    author_id: str
    edit_history_tweet_ids: list[str]
    conversation_id: str
    in_reply_to_user_id: str
    referenced_tweets: list[ReferencedTweets]
    attachments: Attachments
    geo: Geo
    context_annotations: ContextAnnotations
    entities: Entities
    withheld: Withheld
    public_metrics: PublicMetrics
    non_public_metrics: NonPublicMetrics
    organic_metrics: OrganicMetrics
    promoted_metrics: PromotedMetrics
    possibly_sensitive: bool
    lang: str
    reply_settings: str
    source: str
    includes: Includes


class Recent(TypedDict, total=False):
    data: list[Data]
    meta: Meta
    errors: dict[str, str]
