from __future__ import annotations

import abc


class AuthClient(abc.ABC):
    """Abstract of all auth clients."""

    @abc.abstractmethod
    def get_bearer(self) -> str | None:
        """Aquire berer token from Twitter, or return current."""
        raise NotImplementedError()
