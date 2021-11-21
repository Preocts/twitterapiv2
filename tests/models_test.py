"""
Simple tests for all the models

1. Create a mock fixture of the entire model
1. Ensure model builds with `.build_from()`
1. Ensure model returned is instance of BaseModel
1. Ensure model `.to_json()` matches input fixture

"""
import json

import pytest
from twitterapiv2.model.base_model import BaseModel
from twitterapiv2.model.recent.recent import Recent
from twitterapiv2.model.tweet_count.tweet_count import TweetCount


@pytest.mark.parametrize(
    ("model", "fixture_file"),
    (
        (Recent, "tests/fixtures/mock_recent.json"),
        (TweetCount, "tests/fixtures/mock_tweet_count.json"),
    ),
)
def test_model_load_and_serialize(model: BaseModel, fixture_file: str) -> None:
    fixture = json.load(open(fixture_file, "r"))
    built_model = model.build_from(fixture)
    assert isinstance(built_model, BaseModel)

    serialized = built_model.to_json()
    assert serialized == fixture
