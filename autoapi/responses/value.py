import mimetypes
from typing import Union, Dict, List

from autoapi.extensions import ResponseObjectInterface

from marshmallow import Schema, fields


class ValueResponse(ResponseObjectInterface):
    class ValueResponseSchema(Schema):
        value = fields.Field(required=True,
                             validate=(lambda x: type(x) in [int, float, str, bool, dict, list]),
                             description='General value field, can hold an Integer, Float, String, Boolean, Dictionary, or List')

    def __init__(self, value: Union[float, int, str, bool, List, Dict]):
        super().__init__()
        self.value: Union[float, int, str, bool, List, Dict] = value

    def to_dict(self) -> Dict:
        return {
            "value": self.value
        }

    @staticmethod
    def to_schema():
        return ValueResponse.ValueResponseSchema()

    @staticmethod
    def content_type() -> str:
        return mimetypes.MimeTypes().types_map[1]['.json']
