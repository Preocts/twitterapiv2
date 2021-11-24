import vcr
from twitterapiv2.model.recent.recent import Recent
from twitterapiv2.search_recent import SearchRecent

api_recorder = vcr.VCR(
    filter_headers=["Authorization"],
    record_mode="ONCE",
    cassette_library_dir="tests/cassettes/search_recent",
)


@api_recorder.use_cassette()
def test_valid_search() -> None:
    # NOTE: To re-record this test a valid bearer token must be
    # injected into the env. Use the confest autouse fixture.
    client = SearchRecent()
    client.max_results(10)

    result = client.fetch("hello")
    assert isinstance(result, Recent)
    assert result.data
    next_token = client.next_token
    assert next_token

    result = client.fetch("hello", page_token=next_token)
    assert client.next_token != next_token
