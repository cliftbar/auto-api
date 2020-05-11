import inspect
from inspect import Signature
from typing import Dict

from marshmallow import Schema
from webargs import fields

from automd.automd import AutoMD
from automd.decorators import automd
from automd.http_verbs import HTTPVerb
from automd.responses import IntegerResponse, JSONResponse


def test_AutoMD_parse_parameter_schema():
    parameter_schema: Dict = {
        "foo": fields.String(required=True),
        "bar": fields.Integer()
    }

    def func():
        pass

    function_signature: Signature = inspect.signature(func)

    url: str = "/test"
    result_schema: Schema = AutoMD.parse_parameter_schema(parameter_schema, function_signature, url, HTTPVerb.get.value)

    assert list(result_schema.fields.keys()) == ["query"]
    assert result_schema.declared_fields["query"].metadata == {"location": "query", "name": "query"}
    assert list(result_schema.declared_fields["query"].schema.fields.keys()).sort() == ["foo", "bar"].sort()
    assert isinstance(result_schema.declared_fields["query"].schema.fields["foo"], fields.String)
    assert isinstance(result_schema.declared_fields["query"].schema.fields["bar"], fields.Integer)


def test_AutoMD_parse_parameter_no_schema():
    parameter_schema: Dict = None

    def func(foo: str, bar: int):
        pass

    function_signature: Signature = inspect.signature(func)

    url: str = "/test"
    result_schema: Schema = AutoMD.parse_parameter_schema(parameter_schema, function_signature, url, HTTPVerb.get.value)

    assert list(result_schema.fields.keys()) == ["query"]
    assert result_schema.fields["query"].metadata == {"location": "query", "name": "query"}
    assert list(result_schema.fields["query"].schema.fields.keys()).sort() == ["foo", "bar"].sort()
    assert isinstance(result_schema.fields["query"].schema.fields["foo"], fields.String)
    assert isinstance(result_schema.fields["query"].schema.fields["bar"], fields.Integer)


def test_AutoMD_parse_response_integer_object():
    response_object: IntegerResponse = IntegerResponse(10)

    url: str = "/test"
    result_schema: Schema
    content_type: str
    result_schema, content_type = AutoMD.parse_response_schema(response_object,
                                                               url,
                                                               HTTPVerb.get.value)

    assert list(result_schema.fields.keys()) == ["value"]
    assert isinstance(result_schema.fields["value"], fields.Integer)
    assert content_type == "text/plain"


def test_AutoMD_parse_response_str_type():
    url: str = "/test"
    result_schema: Schema
    content_type: str
    result_schema, content_type = AutoMD.parse_response_schema(str,
                                                               url,
                                                               HTTPVerb.get.value)

    assert list(result_schema.fields.keys()) == ["value"]
    assert isinstance(result_schema.fields["value"], fields.String)
    assert content_type == "text/plain"


def test_AutoMD_parse_response_json_object():
    url: str = "/test"
    result_schema: Schema
    content_type: str
    result_schema, content_type = AutoMD.parse_response_schema(JSONResponse,
                                                               url,
                                                               HTTPVerb.get.value)

    assert list(result_schema.fields.keys()) == ["value"]
    assert isinstance(result_schema.fields["value"], fields.Field)
    assert content_type == "application/json"


def test_AutoMD_parse_response_dict_type():
    url: str = "/test"
    result_schema: Schema
    content_type: str
    result_schema, content_type = AutoMD.parse_response_schema(Dict,
                                                               url,
                                                               HTTPVerb.get.value)

    assert list(result_schema.fields.keys()) == ["response"]
    assert isinstance(result_schema.fields["response"], fields.Field)
    assert content_type == "application/json"
