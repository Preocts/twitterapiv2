import logging
import os
from datetime import datetime
from secrets import token_urlsafe
from typing import Dict
from typing import Optional
from urllib import parse

from twitterapiv2.http import Http

BASE_URL = "https://api.twitter.com"


class UserAuthClient:
    def __init__(self, callback_http: str = "https://localhost") -> None:
        self.log = logging.getLogger(__name__)
        self.http = Http()
        self.base_fields = {"callback_http": callback_http}

    def key_collect(self) -> Dict[str, str]:
        """Collect all keys needed for headers"""
        consumer_key = os.getenv("TW_CONSUMER_KEY", None)
        access_token = os.getenv("TW_ACCESS_TOKEN", None)
        if consumer_key is None or access_token is None:
            raise KeyError("Missing consumer/access environment variable(s).")

        keys = {
            "oauth_consumer_key": consumer_key,
            "oauth_nonce": token_urlsafe(),
            "oauth_signature": "",
            "oauth_signature_method": "HMAC-SHA1",
            "oauth_timestamp": f"{int(datetime.utcnow().timestamp())}",
            "oauth_token": access_token,
            "oauth_version": "1.0",
        }
        return keys

    def generate_signature_base_string(
        self,
        method: str,
        route: str,
        keys: Dict[str, str],
        fields: Optional[Dict[str, str]] = None,
    ) -> str:
        """Generate Oauth1 signature base string"""
        if fields is None:
            fields = {}
        fields = {**self.base_fields, **fields, **keys}
        parameter_string = ""
        for field in sorted(fields):
            parameter_string += "&" if parameter_string else ""
            parameter_string += parse.quote_plus(field)
            parameter_string += "="
            parameter_string += parse.quote_plus(fields[field])

        base_string = f"{method.upper()}&"
        base_string += parse.quote_plus(f"{BASE_URL}{route}") + "&"
        base_string += parameter_string

        return base_string
