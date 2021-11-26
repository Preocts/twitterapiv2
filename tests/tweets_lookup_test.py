import pytest
import vcr
from twitterapiv2.model.recent.data import Data
from twitterapiv2.tweets_lookup import TweetsLookup

api_recorder = vcr.VCR(
    filter_headers=["Authorization"],
    record_mode="ONCE",
    cassette_library_dir="tests/cassettes/tweets_lookup",
)

LUCKY_ID = "1461880347478528007"
LUCKY_IDS = "1461880347478528007, 1461880346580979715"


@api_recorder.use_cassette()
def test_valid_single_search() -> None:
    # NOTE: To re-record this test a valid bearer token must be
    # injected into the env. Use the confest autouse fixture.
    client = TweetsLookup()
    client.ids(LUCKY_ID)
    result = client.fetch()
    assert result
    assert len(result) == 1
    assert isinstance(result[0], Data)


@api_recorder.use_cassette()
def test_valid_multi_search() -> None:
    # NOTE: To re-record this test a valid bearer token must be
    # injected into the env. Use the confest autouse fixture.
    client = TweetsLookup()
    client.ids(LUCKY_IDS)
    result = client.fetch()
    assert len(result) == 2


def test_id_required() -> None:
    client = TweetsLookup()
    with pytest.raises(ValueError):
        client.fetch()
