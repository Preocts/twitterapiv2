from __future__ import annotations

from typing import Any

from httpx import Response


class HttpMocker:
    def __init__(self) -> None:
        self._urls: list[str] = []
        self._responses: list[Response] = []

    def add_response(
        self,
        content: str | bytes,
        headers: dict[str, str],
        status_code: int,
        url: str,
    ) -> None:
        self._responses.append(Response(status_code, headers=headers, content=content))
        self._urls.append(url)

    def get(self, *args: Any, **kwargs: Any) -> Response:
        url = self._urls.pop(0)
        resp = self._responses.pop(0)
        assert kwargs["url"] == url

        return resp

    post = get
