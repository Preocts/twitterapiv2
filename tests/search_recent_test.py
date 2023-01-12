from __future__ import annotations

from collections.abc import Generator
from unittest.mock import patch

import pytest
from twitterapiv2.search_recent import SearchRecent
from twitterapiv2.search_recent import URL

from tests.fixtures.clientmocker import ClientMocker
from tests.fixtures.mock_headers import HEADERS

MOCK_RESP = '{"data":[{"id":"1461880347478528007","text":"RT @forlalisa_th: Hello  @BigReidRadio I would LOVE to hear #MONEY  on @997now !! Can you please play \\uD83D\\uDCB8\\uD83D\\uDCB8 for us ?\\uD83E\\uDD70\\uD83D\\uDE01 \\nThank youuuuu!\\uD83E\\uDD17 https:…"},{"id":"1461880346580979715","text":"RT @SAVY13479352: Hello, I am a retired man, trying my best to do Affiliate Marketing, Since last few months I have not received a single s…"},{"id":"1461880346165788678","text":"Hello @God it’s me, I love it here. Thank you."},{"id":"1461880345511432193","text":"RT @skjnkim_cart: [#skjnkim_sells] \\nwts • lfb • ph • nct dream\\n\\n･ᴗ･ Hello Future PCS\\n       •jaemin (future) - clean\\n       •jeno (future)…"},{"id":"1461880344974540805","text":"hello someone pspspspsp https://t.co/qVLlxCEBA4"},{"id":"1461880344026746884","text":"RT @lizehtriosreal: Hello ❤️ https://t.co/gf88tYT4QD"},{"id":"1461880343821176837","text":"RT @mom_tho: hello darkness my old friend\\nis it 5 or 10 pm"},{"id":"1461880343695290368","text":"RT @_naminaminaeee: hello, drop the tags for jihyo!!"},{"id":"1461880343229878276","text":"@NaughtyLoise Hello Tom New Jersey"},{"id":"1461880343020060673","text":"@Hello_Easyaim す"}],"meta":{"newest_id":"1461880347478528007","oldest_id":"1461880343020060673","result_count":10,"next_token":"b26v89c19zqg8o3fpdy5zsnp3n3qzp909cim472adoxa5"}}'  # noqa: E501


@pytest.fixture
def client() -> Generator[SearchRecent, None, None]:
    search_client = SearchRecent()
    with patch.object(search_client, "http", ClientMocker()):
        yield search_client


def test_valid_search(client: SearchRecent) -> None:
    # TODO: These are flagging as type errors in editor
    client.http.add_response(MOCK_RESP, HEADERS, 200, URL)

    client.max_results(10)
    client.query("hello")
    result = client.fetch()
    assert result["data"]


def test_query_required() -> None:
    client = SearchRecent()
    with pytest.raises(ValueError):
        client.fetch()
