from __future__ import annotations

from typing import Any

from twitterapiv2.model.base_model import BaseModel


class ResponseHeader(BaseModel):
    """Empty Twitter v2 Response Header"""

    date: str
    server: str
    set_cookie: str
    api_version: str
    content_type: str
    cache_control: str
    content_length: str
    x_access_level: str
    x_frame_options: str
    x_xss_protection: str
    x_rate_limit_limit: str
    x_rate_limit_reset: str
    content_disposition: str
    x_content_type_options: str
    x_rate_limit_remaining: str
    strict_transport_security: str
    x_response_time: str
    x_connection_hash: str

    @classmethod
    def build_from(cls, data: dict[str, Any]) -> ResponseHeader:
        """Provide urllib3 HTTPResponse object"""
        new = cls()
        new.date = data.get("date", "")
        new.server = data.get("server", "")
        new.set_cookie = data.get("set-cookie", "")
        new.api_version = data.get("api-version", "")
        new.content_type = data.get("content-type", "")
        new.cache_control = data.get("cache-control", "")
        new.content_length = data.get("content-length", "")
        new.x_access_level = data.get("x-access-level", "")
        new.x_frame_options = data.get("x-frame-options", "")
        new.x_xss_protection = data.get("x-xss-protection", "")
        new.x_rate_limit_limit = data.get("x-rate-limit-limit", "")
        new.x_rate_limit_reset = data.get("x-rate-limit-reset", "")
        new.content_disposition = data.get("content-disposition", "")
        new.x_content_type_options = data.get("x-content-type-options", "")
        new.x_rate_limit_remaining = data.get("x-rate-limit-remaining", "")
        new.strict_transport_security = data.get("strict-transport-security", "")
        new.x_response_time = data.get("x-response-time", "")
        new.x_connection_hash = data.get("x-connection-hash", "")
        return new
