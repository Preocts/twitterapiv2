from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class ApplicationAuth:
    """Authentication keys for application only OAuth clients."""

    consumer_key: str
    consumer_secret: str
    consumer_bearer: str | None = None

    @classmethod
    def from_environ(cls) -> ApplicationAuth:
        """
        Build Authentication keys from environment variables.

        Environments Variables:
            TW_CONSUMER_KEY: required
            TW_CONSUMER_SECRET: required
            TW_CONSUMER_BEARER: optional
        """
        return cls(
            consumer_key=os.environ["TW_CONSUMER_KEY"],
            consumer_secret=os.environ["TW_CONSUMER_SECRET"],
            consumer_bearer=os.getenv("TW_CONSUMER_BEARER"),
        )
