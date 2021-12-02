import base64
import hmac
import logging
import os
from datetime import datetime
from hashlib import sha1
from secrets import token_urlsafe
from typing import Dict
from typing import List
from urllib import parse

from twitterapiv2.http import Http

BASE_URL = "https://api.twitter.com"


class UserAuthClient:
    def __init__(self, callback_http: str = "https://localhost") -> None:
        self.log = logging.getLogger(__name__)
        self.http = Http()
        self.callback_http = callback_http

    def key_collect(self) -> Dict[str, str]:
        """Collect all keys needed for headers"""
        consumer_key = os.getenv("TW_CONSUMER_KEY", None)
        access_token = os.getenv("TW_ACCESS_TOKEN", None)
        if consumer_key is None or access_token is None:
            raise KeyError("Missing consumer/access environment variable(s).")

        keys = {
            "oauth_consumer_key": consumer_key,
            "oauth_nonce": token_urlsafe(),
            "oauth_signature_method": "HMAC-SHA1",
            "oauth_timestamp": f"{int(datetime.utcnow().timestamp())}",
            "oauth_token": access_token,
            "oauth_version": "1.0",
        }
        return keys

    def generate_parameter_string(self, fields: Dict[str, str]) -> str:
        """Generate OAuth1 parameter string"""
        parameter_segments: List[str] = []
        for field in sorted(fields):
            key = parse.quote(field, safe="")
            value = parse.quote(fields[field], safe="")
            parameter_segments.append(f"{key}={value}")
        return "&".join(parameter_segments)

    def generate_base_string(
        self,
        method: str,
        route: str,
        parameter_string: str,
    ) -> str:
        """Generate OAuth1 base string"""
        base_string = f"{method.upper()}&"
        base_string += parse.quote(f"{BASE_URL}{route}", safe="") + "&"
        base_string += parse.quote(parameter_string, safe="")
        return base_string

    def generate_signature_string(self, base_string: str) -> str:
        """Generate OAuth1 signature"""
        consumer_secret = os.getenv("TW_CONSUMER_SECRET", None)
        access_secret = os.getenv("TW_ACCESS_SECRET", None)
        if consumer_secret is None or access_secret is None:
            raise KeyError("Missing consumer/access environment variable(s).")
        base_bytes = base_string.encode("utf-8")
        combined = (
            parse.quote(consumer_secret, safe="")
            + "&"
            + parse.quote(access_secret, safe="")
        ).encode("utf-8")
        hash_bytes = hmac.new(combined, base_bytes, sha1).digest()
        return base64.encodebytes(hash_bytes).decode("utf-8").rstrip("\n")
