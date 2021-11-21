import json

from twitterapiv2.model.base_model import BaseModel
from twitterapiv2.model.recent.recent import Recent

MOCK_MODEL = json.load(open("tests/fixtures/mock_recent.json", "r"))


def test_apply_model() -> None:
    model = Recent.build_from(MOCK_MODEL)
    assert isinstance(model, BaseModel)


def test_to_json() -> None:
    model = Recent.build_from(MOCK_MODEL)
    serialized = model.to_json()
    assert serialized == MOCK_MODEL
