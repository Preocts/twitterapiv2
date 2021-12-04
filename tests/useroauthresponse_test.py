import pytest
from twitterapiv2.model.useroauthresponse import UserOAuthResponse


USER_RESP = "oauth_token=UsPAbAAAAAABVjj_AAABfYO81xo&oauth_token_secret=mwr3uC5LWlgfYewBMNVTAi1VPlI1BmXL&oauth_callback_confirmed=true"  # noqa
USER_EXPECTED = (
    "UsPAbAAAAAABVjj_AAABfYO81xo",
    "mwr3uC5LWlgfYewBMNVTAi1VPlI1BmXL",
)
ACCESS_RESP = "oauth_token=1069768653757997056-8rVedS0KEQI9KvzLOtamAw0wZixSBB&oauth_token_secret=i3OCVHR0AGXjMrCcrBtedNi89vUm4YovBo67cE8Xaf4z8&user_id=1069768653757997&screen_name=preocts"  # noqa
ACCESS_EXPECTED = (
    "1069768653757997056-8rVedS0KEQI9KvzLOtamAw0wZixSBB",
    "i3OCVHR0AGXjMrCcrBtedNi89vUm4YovBo67cE8Xaf4z8",
    "1069768653757997",
    "preocts",
)


def test_from_user_resp() -> None:
    result = UserOAuthResponse.from_resp_string(USER_RESP)
    assert result.oauth_token == USER_EXPECTED[0]
    assert result.oauth_token_secret == USER_EXPECTED[1]


def test_from_access_resp() -> None:
    result = UserOAuthResponse.from_resp_string(ACCESS_RESP)
    assert result.oauth_token == ACCESS_EXPECTED[0]
    assert result.oauth_token_secret == ACCESS_EXPECTED[1]
    assert result.user_id == ACCESS_EXPECTED[2]
    assert result.screen_name == ACCESS_EXPECTED[3]


def test_raises() -> None:
    with pytest.raises(ValueError):
        UserOAuthResponse.from_resp_string("mock")
