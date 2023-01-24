"""Simple model holding user id, username, and name."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Me:
    """Simple model holding user id, username, and name."""

    id: str  # noqa: A003
    username: str
    name: str
