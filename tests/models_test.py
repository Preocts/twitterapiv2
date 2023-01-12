from __future__ import annotations

import json

import pytest
from twitterapiv2.model.base_model import BaseModel
from twitterapiv2.model.tweet_count.tweet_count import TweetCount


@pytest.mark.parametrize(
    ("model", "fixture_file"),
    ((TweetCount, "tests/fixtures/mock_tweet_count.json"),),
)
def test_model_load_and_serialize(model: BaseModel, fixture_file: str) -> None:
    fixture = json.load(open(fixture_file))
    built_model = model.build_from(fixture)
    assert isinstance(built_model, BaseModel)

    serialized = built_model.to_json()
    assert serialized == fixture
