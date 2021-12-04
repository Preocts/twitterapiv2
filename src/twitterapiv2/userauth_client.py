"""
Authenticate using OAuth1 for user

Creating signature:
https://developer.twitter.com/en/docs/authentication/oauth-1-0a/creating-a-signature

Building header string:
https://developer.twitter.com/en/docs/authentication/oauth-1-0a/authorizing-a-request

3-step Auth process:
https://developer.twitter.com/en/docs/authentication/oauth-1-0a/obtaining-user-access-tokens
https://developer.twitter.com/en/docs/authentication/api-reference/request_token
"""
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
    def __init__(self, callback_http: str = "oob") -> None:
        self.log = logging.getLogger(__name__)
        self.http = Http()
        self.callback_http = callback_http

    def generate_oauth_header(self, header_values: Dict[str, str]) -> str:
        """Generated OAuth header string"""
        segments: List[str] = []
        for key, value in header_values.items():
            qkey = parse.quote(key, safe="")
            qvalue = parse.quote(value, safe="")
            segments.append(f'{qkey}="{qvalue}"')
        return "OAuth " + ", ".join(segments)

    def generate_header_key_values(self) -> Dict[str, str]:
        """Collect all key:values needed for headers excluding `oauth_signature`"""
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

    def request_token(self) -> None:
        """Leg 1 of 3"""
        # TODO : finish work
        raise NotImplementedError("WIP")
        header_values = self.generate_header_key_values()
        fields = {"oauth_callback": self.callback_http, **header_values}
        param = self.generate_parameter_string(fields)
        base = self.generate_base_string("POST", "/oauth/request_token", param)
        header_values["oauth_signature"] = self.generate_signature_string(base)
        headers = {"Authorization": self.generate_oauth_header(header_values)}
        url = f"{BASE_URL}/oauth/request_token?oauth_callback="
        url += parse.quote(self.callback_http)

        result = self.http.http.request("POST", url, headers=headers)
        # result = self.http.post(url, headers=headers)
        oauth_token, oauth_secret, _ = result.data.decode("utf-8").split("&", 3)
        print("Go here next:")
        print(f"https://api.twitter.com/oauth/authorize?oauth_token={oauth_token}")


if __name__ == "__main__":
    from secretbox import SecretBox

    logging.basicConfig(level="DEBUG")
    box = SecretBox(auto_load=True)
    client = UserAuthClient()
    client.request_token()
