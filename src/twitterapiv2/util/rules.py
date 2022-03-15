from __future__ import annotations

import re
from datetime import datetime

ISO8601_PATTERN = r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z?$"


def is_ISO8601(dt_string: str | None) -> bool:
    """Assert that datetime string is valid ISO8601 UTC time"""
    return bool(re.match(ISO8601_PATTERN, dt_string or ""))


def to_ISO8601(dt: datetime) -> str:
    """Convert datetime object to ISO 8601 standard UTC string"""
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
