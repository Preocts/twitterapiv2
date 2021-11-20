import json

from twitterapiv2.model.recent.recent import Recent

MOCK_MODEL = json.load(open("tests/fixtures/mock_model.json", "r"))


def test_apply_model() -> None:
    model = Recent.build_obj(MOCK_MODEL)
    assert isinstance(model, Recent)
