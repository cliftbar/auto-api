from typing import Dict

from automd.encoder import AutoMDObjEncoder


def test_AutoMDObjEncoder():
    class TestSerializableObject:
        def __init__(self):
            pass

        def to_dict(self):
            return {
                "key": "value"
            }

    test_class: TestSerializableObject = TestSerializableObject()
    encoder: AutoMDObjEncoder = AutoMDObjEncoder()

    json_serialize: Dict = encoder.default(test_class)

    assert json_serialize == {"key": "value"}
