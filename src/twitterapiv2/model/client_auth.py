from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class ClientAuth:
    """Authentication keys for client OAuth2 authorization."""

    client_id: str
    client_secret: str | None = None
    redirect_uri: str = "https://127.0.0.1"

    @classmethod
    def from_environ(cls) -> ClientAuth:
        """
        Build ClientAuth from environment variables.

        Environments Variables:
            TW_CLIENT_ID: required
            TW_CLIENT_SECRET: optional (confidential versus public auth)
            TW_REDIRECT_URL: optional (default: https://127.0.0.1)
        """
        return cls(
            client_id=os.environ["TW_CLIENT_ID"],
            client_secret=os.environ.get("TW_CLIENT_SECRET"),
            redirect_uri=os.environ.get("TW_REDIRECT_URI", "https://127.0.0.1"),
        )
