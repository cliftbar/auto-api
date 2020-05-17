import inspect
import typing
from typing import List, Dict
from inspect import Signature

from marshmallow import fields

from automd.responses.responses import (map_response_object_type,
                                        StringResponse,
                                        IntegerResponse,
                                        FloatResponse,
                                        DictResponse,
                                        ListResponse,
                                        ValueResponse, map_type_field_mapping, recursive_one)


def test_map_response_object_type_str():
    assert map_response_object_type("str") == StringResponse
    assert map_response_object_type(str) == StringResponse


def test_map_response_object_type_int():
    assert map_response_object_type("int") == IntegerResponse
    assert map_response_object_type(int) == IntegerResponse


def test_map_response_object_type_float():
    assert map_response_object_type("float") == FloatResponse
    assert map_response_object_type(float) == FloatResponse


def test_map_response_object_type_dict():
    class SomeObject:
        pass

    assert map_response_object_type("dict") == DictResponse
    assert map_response_object_type(dict) == DictResponse
    assert map_response_object_type(typing.Dict) == DictResponse
    assert map_response_object_type(typing.Dict[str, int]) == DictResponse
    assert map_response_object_type(typing.Dict[SomeObject, typing.List]) == DictResponse
    assert map_response_object_type(getattr(typing.Dict, "_name", "Dict._name")) == DictResponse
    assert map_response_object_type(getattr(typing.Dict, "_gorg", "Dict._gorg")) == DictResponse
    assert map_response_object_type("Dict") == DictResponse


def test_map_response_object_type_list():
    class SomeObject:
        pass

    assert map_response_object_type("list") == ListResponse
    assert map_response_object_type(list) == ListResponse
    assert map_response_object_type(typing.List) == ListResponse
    assert map_response_object_type(typing.List[str]) == ListResponse
    assert map_response_object_type(typing.List[SomeObject]) == ListResponse
    assert map_response_object_type(getattr(typing.List, "_name", "List._name")) == ListResponse
    assert map_response_object_type(getattr(typing.List, "_gorg", "List._gorg")) == ListResponse
    assert map_response_object_type("List") == ListResponse


def test_map_response_object_type_none():
    assert map_response_object_type(Signature.empty) is None
    assert map_response_object_type(None) is None


def test_map_response_object_type_any():
    assert map_response_object_type("Any") == ValueResponse
    assert map_response_object_type(typing.Any) == ValueResponse
    assert map_response_object_type(getattr(typing.Any, "_name", "Any._name")) == ValueResponse
    assert map_response_object_type(getattr(typing.Any, "_gorg", "Any._gorg")) == ValueResponse


##########################
# map_type_field_mapping #
##########################
def test_map_type_field_mapping_str():
    assert map_type_field_mapping("str") == fields.String
    assert map_type_field_mapping(str) == fields.String


def test_map_type_field_mapping_bool():
    assert map_type_field_mapping("bool") == fields.Boolean
    assert map_type_field_mapping(bool) == fields.Boolean


def test_map_type_field_mapping_int():
    assert map_type_field_mapping("int") == fields.Integer
    assert map_type_field_mapping(int) == fields.Integer


def test_map_type_field_mapping_float():
    assert map_type_field_mapping("float") == fields.Float
    assert map_type_field_mapping(float) == fields.Float


def test_map_type_field_mapping_dict():
    class SomeObject:
        pass

    assert map_type_field_mapping("dict") == fields.Dict
    assert map_type_field_mapping(dict) == fields.Dict
    assert map_type_field_mapping(typing.Dict) == fields.Dict
    assert map_type_field_mapping(typing.Dict[str, int]) == fields.Dict
    assert map_type_field_mapping(typing.Dict[SomeObject, typing.List]) == fields.Dict
    assert map_type_field_mapping(getattr(typing.Dict, "_name", "Dict._name")) == fields.Dict
    assert map_type_field_mapping(getattr(typing.Dict, "_gorg", "Dict._gorg")) == fields.Dict
    assert map_type_field_mapping("Dict") == fields.Dict


def test_map_type_field_mapping_list():
    class SomeObject:
        pass

    assert map_type_field_mapping("list") == fields.List
    assert map_type_field_mapping(list) == fields.List
    assert map_type_field_mapping(typing.List) == fields.List
    assert map_type_field_mapping(typing.List[str]) == fields.List
    assert map_type_field_mapping(typing.List[SomeObject]) == fields.List
    assert map_type_field_mapping(getattr(typing.List, "_name", "List._name")) == fields.List
    assert map_type_field_mapping(getattr(typing.List, "_gorg", "List._gorg")) == fields.List
    assert map_type_field_mapping("List") == fields.List


def test_map_type_field_mapping_none():
    assert map_type_field_mapping(None) is None


def test_map_type_field_mapping_any():
    assert map_type_field_mapping("Any") == fields.Raw
    assert map_type_field_mapping(typing.Any) == fields.Raw
    assert map_type_field_mapping(getattr(typing.Any, "_name", "Any._name")) == fields.Raw
    assert map_type_field_mapping(getattr(typing.Any, "_gorg", "Any._gorg")) == fields.Raw
    assert map_type_field_mapping(Signature.empty) is fields.Raw


class TestResponsesTypeToField:
    def test_any(self):
        field: fields.Field = recursive_one(typing.Any)

        assert isinstance(field, fields.Raw)

    def test_empty(self):
        field: fields.Field = recursive_one(inspect.Signature.empty)

        assert isinstance(field, fields.Raw)

    def test_bool(self):
        field: fields.Field = recursive_one(bool)

        assert isinstance(field, fields.Boolean)

    def test_int(self):
        field: fields.Field = recursive_one(int)

        assert isinstance(field, fields.Integer)

    def test_float(self):
        field: fields.Field = recursive_one(float)

        assert isinstance(field, fields.Float)

    def test_str(self):
        field: fields.Field = recursive_one(str)

        assert isinstance(field, fields.String)

    def test_union_basic(self):
        field: fields.Field = recursive_one(typing.Union[str, int])

        assert isinstance(field, fields.Raw)
        assert field.metadata["description"] == "Multiple Types Allowed: <class 'str'>, <class 'int'>"

    def test_list(self):
        field: fields.Field = recursive_one(typing.List)

        assert isinstance(field, fields.List)
        assert isinstance(field.inner, fields.Raw)

    def test_list_complex(self):
        field: fields.Field = recursive_one(List[List])

        assert type(field) == fields.List
        assert type(field.inner) == fields.List
        assert type(field.inner.inner) == fields.Raw

    def test_dict(self):
        field: fields.Field = recursive_one(Dict)

        assert isinstance(field, fields.Dict)
        assert isinstance(field.key_field, fields.Raw)
        assert isinstance(field.value_field, fields.Raw)

    def test_dict_complex(self):
        field: fields.Field = recursive_one(Dict[str, int])

        assert isinstance(field, fields.Dict)
        assert isinstance(field.key_field, fields.String)
        assert isinstance(field.value_field, fields.Integer)

    def test_optional(self):
        field: fields.Field = recursive_one(typing.Optional[str])

        assert isinstance(field, fields.String)

    def test_optional_complex(self):
        field: fields.Field = recursive_one(typing.Optional[List[str]])

        assert isinstance(field, fields.List)
        assert isinstance(field.inner, fields.String)

    def test_union(self):
        field: fields.Field = recursive_one(typing.Union[int, str])

        assert isinstance(field, fields.Raw)
        assert field.metadata["description"] == "Multiple Types Allowed: <class 'int'>, <class 'str'>"

    def test_union_complex(self):
        field: fields.Field = recursive_one(typing.Union[typing.List[str], Dict[str, bool]])

        assert isinstance(field, fields.Raw)
        assert field.metadata["description"] == "Multiple Types Allowed: typing.List[str], typing.Dict[str, bool]"
