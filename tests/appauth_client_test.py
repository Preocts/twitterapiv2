import os
from unittest.mock import patch

import pytest
from twitterapiv2.appauth_client import AppAuthClient


MOCK_KEY = "xvz1evFS4wEEPTGEFPHBog"
MOCK_SECRET = "L8qq9PZyRg6ieKGEKhZolGC0vJWLw8iEJ88DRdyOg"
MOCK_CRED = "eHZ6MWV2RlM0d0VFUFRHRUZQSEJvZzpMOHFxOVBaeVJnNmllS0dFS2hab2xHQzB2SldMdzhpRUo4OERSZHlPZw=="  # noqa


def test_encoded_credentials() -> None:
    client = AppAuthClient()
    env = {
        "TW_CONSUMER_KEY": MOCK_KEY,
        "TW_CONSUMER_SECRET": MOCK_SECRET,
    }
    with patch.dict(os.environ, env):
        result = client.encoded_credentials()
        assert result == MOCK_CRED


def test_require_environ_vars() -> None:
    client = AppAuthClient()
    os.environ.pop("TW_CONSUMER_KEY", None)
    with pytest.raises(KeyError):
        client.encoded_credentials()

    os.environ["TW_CONSUMER_KEY"] = "Mock"
    os.environ.pop("TW_CONSUMER_SECRET", None)
    with pytest.raises(KeyError):
        client.encoded_credentials()


def test_set_bearer_token() -> None:
    # NOTE: To re-record this test you need to inject valid creds to conftest
    assert os.getenv("TW_BEARER_TOKEN") is None
    client = AppAuthClient()

    token = client.fetch_bearer_token()
    assert os.getenv("TW_BEARER_TOKEN") is None

    client.set_bearer_token()
    assert os.environ["TW_BEARER_TOKEN"] == token


def test_revoke_bearer_token() -> None:
    # NOTE: To re-record this test you need to inject valid creds to conftest

    # assert os.getenv("TW_BEARER_TOKEN") is None
    client = AppAuthClient()
    # TODO: (preocts) This endpoint does't work. No response from Twitter
    with pytest.raises(NotImplementedError):
        client.revoke_bearer_token()
    # client.set_bearer_token()
    # assert os.environ["TW_BEARER_TOKEN"]
    # client.revoke_bearer_token()
    # assert os.getenv("TW_BEARER_TOKEN") is None


def test_invalid_bearer_request() -> None:
    client = AppAuthClient()
    with pytest.raises(ValueError):
        client.set_bearer_token()


def test_invalid_bearer_response() -> None:
    # NOTE: Uses edited valid recording missing access_token
    client = AppAuthClient()
    with pytest.raises(ValueError):
        client.set_bearer_token()
