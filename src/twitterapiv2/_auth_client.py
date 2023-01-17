from __future__ import annotations

import abc
from typing import Any


class AuthClient(abc.ABC):
    """Abstract for all auth clients."""

    @abc.abstractmethod
    def __init__(self, auth_model: Any, scopes: list[str]) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_bearer(self) -> str | None:
        raise NotImplementedError()
