import pytest
from twitterapiv2.model.recent.recent import Recent
from twitterapiv2.search_recent import SearchRecent


def test_valid_search() -> None:
    # NOTE: To re-record this test a valid bearer token must be
    # injected into the env. Use the confest autouse fixture.
    client = SearchRecent()

    client.max_results(10)
    client.query("hello")
    result = client.fetch()
    assert isinstance(result, Recent)
    assert result.data

    next_token = client.fields.get("next_token")
    assert next_token
    assert client.more

    result = client.fetch()
    assert client.fields.get("next_token") != next_token


def test_query_required() -> None:
    client = SearchRecent()
    with pytest.raises(ValueError):
        client.fetch()
