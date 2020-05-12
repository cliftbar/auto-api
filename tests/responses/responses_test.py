import typing
from inspect import Signature

from automd.responses.responses import (map_response_object_type,
                                        StringResponse,
                                        IntegerResponse,
                                        FloatResponse,
                                        DictResponse,
                                        ListResponse,
                                        ValueResponse)


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
