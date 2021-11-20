import os
from typing import Generator
from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def mask_environ() -> Generator[None, None, None]:
    """Mask existing creds in environment - used on all tests"""
    with patch.dict(os.environ):
        # NOTE: Set these to actual creds ONLY during re-recording of cassettes
        os.environ["TW_CONSUMER_KEY"] = "MOCK"
        os.environ["TW_CONSUMER_SECRET"] = "MOCK"
        os.environ.pop("TW_BEARER_TOKEN", None)
        yield None
