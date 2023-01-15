from __future__ import annotations

import os
from unittest.mock import patch

import pytest
from twitterapiv2.model.client_auth import ClientAuth


def test_from_environ() -> None:
    mock_env = {
        "TW_CLIENT_ID": "mockid",
        "TW_CLIENT_SECRET": "mocksecret",
    }

    with patch.dict(os.environ, mock_env):
        auth = ClientAuth.from_environ()

    assert auth.client_id == "mockid"
    assert auth.client_secret == "mocksecret"


def test_from_environ_raises_keyerror() -> None:
    with patch.dict(os.environ, {}):
        os.environ.pop("TW_CLIENT_ID", None)
        os.environ.pop("TW_CLIENT_SECRET", None)

        with pytest.raises(KeyError):
            ClientAuth.from_environ()
