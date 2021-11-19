from typing import Any


class ResponseHeader:
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
    def build_from(cls, data: Any) -> "ResponseHeader":
        """Provide urllib3 HTTPResponse object"""
        new = cls()
        new.date = data.getheader("date", "")
        new.server = data.getheader("server", "")
        new.set_cookie = data.getheader("set-cookie", "")
        new.api_version = data.getheader("api-version", "")
        new.content_type = data.getheader("content-type", "")
        new.cache_control = data.getheader("cache-control", "")
        new.content_length = data.getheader("content-length", "")
        new.x_access_level = data.getheader("x-access-level", "")
        new.x_frame_options = data.getheader("x-frame-options", "")
        new.x_xss_protection = data.getheader("x-xss-protection", "")
        new.x_rate_limit_limit = data.getheader("x-rate-limit-limit", "")
        new.x_rate_limit_reset = data.getheader("x-rate-limit-reset", "")
        new.content_disposition = data.getheader("content-disposition", "")
        new.x_content_type_options = data.getheader("x-content-type-options", "")
        new.x_rate_limit_remaining = data.getheader("x-rate-limit-remaining", "")
        new.strict_transport_security = data.getheader("strict-transport-security", "")
        new.x_response_time = data.getheader("x-response-time", "")
        new.x_connection_hash = data.getheader("x-connection-hash", "")
        return new
