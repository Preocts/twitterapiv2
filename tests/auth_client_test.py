import os
from unittest.mock import patch

import pytest
import vcr
from twitterapiv2.auth_client import AuthClient


MOCK_KEY = "xvz1evFS4wEEPTGEFPHBog"
MOCK_SECRET = "L8qq9PZyRg6ieKGEKhZolGC0vJWLw8iEJ88DRdyOg"
MOCK_CRED = "eHZ6MWV2RlM0d0VFUFRHRUZQSEJvZzpMOHFxOVBaeVJnNmllS0dFS2hab2xHQzB2SldMdzhpRUo4OERSZHlPZw=="  # noqa

api_recorder = vcr.VCR(
    filter_headers=["Authorization"],
    record_mode="ONCE",
    cassette_library_dir="tests/cassettes/auth_client",
)


def test_encoded_credentials() -> None:
    client = AuthClient()
    env = {
        "TW_CONSUMER_KEY": MOCK_KEY,
        "TW_CONSUMER_SECRET": MOCK_SECRET,
    }
    with patch.dict(os.environ, env):
        result = client.encoded_credentials()
        assert result == MOCK_CRED


def test_require_environ_vars() -> None:
    client = AuthClient()
    os.environ.pop("TW_CONSUMER_KEY", None)
    with pytest.raises(KeyError):
        client.encoded_credentials()

    os.environ["TW_CONSUMER_KEY"] = "Mock"
    os.environ.pop("TW_CONSUMER_SECRET", None)
    with pytest.raises(KeyError):
        client.encoded_credentials()


@api_recorder.use_cassette()
def test_set_bearer_token() -> None:
    # NOTE: To re-record this test you need to inject valid creds to conftest
    assert os.getenv("TW_BEARER_TOKEN") is None
    client = AuthClient()
    client.set_bearer_token()
    assert os.environ["TW_BEARER_TOKEN"]


@api_recorder.use_cassette()
def test_invalid_bearer_request() -> None:
    client = AuthClient()
    with pytest.raises(ValueError):
        client.set_bearer_token()


@api_recorder.use_cassette()
def test_invalid_bearer_response() -> None:
    # NOTE: Uses edited valid recording missing access_token
    client = AuthClient()
    with pytest.raises(ValueError):
        client.set_bearer_token()
