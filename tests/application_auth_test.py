from __future__ import annotations

import os
from unittest.mock import patch

import pytest
from twitterapiv2.model.application_auth import ApplicationAuth


def test_from_environ() -> None:
    mock_env = {
        "TW_CONSUMER_KEY": "mockkey",
        "TW_CONSUMER_SECRET": "mocksecret",
        "TW_CONSUMER_BEARER": "mockbearer",
    }

    with patch.dict(os.environ, mock_env):
        auth = ApplicationAuth.from_environ()

    assert auth.consumer_key == "mockkey"
    assert auth.consumer_secret == "mocksecret"
    assert auth.consumer_bearer == "mockbearer"


def test_from_environ_raises_keyerror() -> None:
    with patch.dict(os.environ, {}):
        os.environ.pop("TW_CONSUMER_KEY", None)
        os.environ.pop("TW_CONSUMER_SECRET", None)
        os.environ.pop("TW_CONSUMER_BEARER", None)

        with pytest.raises(KeyError):
            ApplicationAuth.from_environ()
