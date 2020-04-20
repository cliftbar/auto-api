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


class ListResponse(ResponseObjectInterface):
    class ListResponseSchema(Schema):
        value = fields.List(fields.Raw(),
                            required=True,
                            description='List Response')

    def __init__(self, value: List):
        super().__init__()
        self.value: List = value

    def to_dict(self) -> Dict:
        return {
            "value": self.value
        }

    @staticmethod
    def to_schema():
        return ListResponse.ListResponseSchema()

    @staticmethod
    def content_type() -> str:
        return mimetypes.MimeTypes().types_map[1]['.txt']


class DictResponse(ResponseObjectInterface):
    class DictResponseSchema(Schema):
        response = fields.Dict(required=True,
                               description='Dict Response')

    def __init__(self,
                 value: dict):
        super().__init__()
        self.value: dict = value

    def to_dict(self) -> Dict:
        return {
            "value": self.value
        }

    @staticmethod
    def to_schema():
        return DictResponse.DictResponseSchema()

    @staticmethod
    def content_type() -> str:
        return mimetypes.MimeTypes().types_map[1]['.json']


class JSONResponse(ResponseObjectInterface):
    class JSONResponseSchema(Schema):
        value = fields.Field(required=True,
                             validate=(lambda x: type(x) in [dict, list]),
                             description='JSON Response')

    def __init__(self,
                 value: Union[List, Dict]):
        super().__init__()
        self.value: Union[List, Dict] = value

    def to_dict(self) -> Dict:
        return {
            "value": self.value
        }

    @staticmethod
    def to_schema():
        return JSONResponse.JSONResponseSchema()

    @staticmethod
    def content_type() -> str:
        return mimetypes.MimeTypes().types_map[1]['.json']


class StringResponse(ResponseObjectInterface):
    class StringResponseSchema(Schema):
        value = fields.String(required=True,
                              description='String Response')

    def __init__(self,
                 value: str):
        super().__init__()
        self.value: str = value

    def to_dict(self) -> Dict:
        return {
            "value": self.value
        }

    @staticmethod
    def to_schema():
        return StringResponse.StringResponseSchema()

    @staticmethod
    def content_type() -> str:
        return mimetypes.MimeTypes().types_map[1]['.txt']


class IntegerResponse(ResponseObjectInterface):
    class IntegerResponseSchema(Schema):
        value = fields.Integer(required=True,
                               description='Integer Response')

    def __init__(self,
                 value: int):
        super().__init__()
        self.value: int = value

    def to_dict(self) -> Dict:
        return {
            "value": self.value
        }

    @staticmethod
    def to_schema():
        return IntegerResponse.IntegerResponseSchema()

    @staticmethod
    def content_type() -> str:
        return mimetypes.MimeTypes().types_map[1]['.txt']


response_object_type_map: Dict = {
    int: IntegerResponse,
    "int": IntegerResponse,
    str: StringResponse,
    "str": StringResponse,
    list: ListResponse,
    List: ListResponse,
    "List": ListResponse,
    dict: DictResponse,
    Dict: DictResponse,
    "Dict": DictResponse
}