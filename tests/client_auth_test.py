from __future__ import annotations

import os
from unittest.mock import patch

import pytest
from twitterapiv2.model.client_auth import ClientAuth


def test_from_environ() -> None:
    mock_env = {
        "TW_CLIENT_ID": "mockid",
        "TW_CLIENT_SECRET": "mocksecret",
        "TW_REDIRECT_URI": "https://example.com",
    }

    with patch.dict(os.environ, mock_env):
        auth = ClientAuth.from_environ()

    assert auth.client_id == "mockid"
    assert auth.client_secret == "mocksecret"
    assert auth.redirect_uri == "https://example.com"


def test_from_environ_optionals() -> None:
    mock_env = {"TW_CLIENT_ID": "mockid"}

    with patch.dict(os.environ, mock_env):
        os.environ.pop("TW_CLIENT_SECRET", None)
        os.environ.pop("TW_REDIRECT_URI", None)

        auth = ClientAuth.from_environ()

    assert auth.client_id == "mockid"
    assert auth.client_secret is None
    assert auth.redirect_uri == "https://127.0.0.1"


def test_from_environ_raises_keyerror() -> None:
    with patch.dict(os.environ, {}):
        os.environ.pop("TW_CLIENT_ID", None)
        os.environ.pop("TW_CLIENT_SECRET", None)
        os.environ.pop("TW_REDIRECT_URI", None)

        with pytest.raises(KeyError):
            ClientAuth.from_environ()
