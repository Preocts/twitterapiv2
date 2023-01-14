from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ApplicationAuth:
    """Authentication keys for application only OAuth clients."""

    consumer_key: str
    consumer_secret: str
    consumer_bearer: str | None = None
