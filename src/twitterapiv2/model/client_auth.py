from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class ClientAuth:
    """Authentication keys for client OAuth2 authorization."""

    client_id: str
    client_secret: str | None

    @classmethod
    def from_environ(cls) -> ClientAuth:
        """
        Build ClientAuth from environment variables.

        Environments Variables:
            TW_CLIENT_ID: required
            TW_CLIENT_SECRET: optional (confidential versus public auth)
        """
        return cls(
            client_id=os.environ["TW_CLIENT_ID"],
            client_secret=os.environ.get("TW_CLIENT_SECRET"),
        )
