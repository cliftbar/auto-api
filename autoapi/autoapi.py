import mimetypes
from http.client import responses
from typing import Dict, Union

from winmagic import magic
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_restful import Api
from marshmallow import Schema
from marshmallow.fields import Field

from autoapi.encoder import AutoAPIObjEncoder
from autoapi.extensions import ResponseObjectInterface


class AutoAPI:
    config_key: str = "AutoAPI"
    function_key = "autoapi_spec"

    def __init__(self, app_api: Api, title, version, openapi_version, info: Dict = None):
        self.app_api = app_api

        self.apispec_options: Dict = {
            "title": title,
            "version": version,
            "openapi_version": openapi_version,
            "info": {} if info is None else info,
            "plugins": [MarshmallowPlugin()]
        }

        self.app_api.app.config[AutoAPI.config_key] = self

        self.app_api.app.config['RESTFUL_JSON'] = {'cls': AutoAPIObjEncoder}

    @staticmethod
    def build_schema_spec(schema: Dict):
        ret = {
            'parameters': [],
        }

        key: str
        value: Field
        for key, value in schema.items():
            arg_in = value.metadata.get('location')
            if arg_in == 'json':
                continue
            required = value.required
            name = value.name or key
            description = value.metadata.get('description')

            ret['parameters'].append({
                'name': name,
                "in": arg_in,
                'required': required,
                'description': description
            })

        return ret

    def build_spec(self) -> APISpec:
        api_spec: APISpec = APISpec(self.apispec_options["title"],
                                    self.apispec_options["version"],
                                    self.apispec_options["openapi_version"],
                                    info=self.apispec_options["info"],
                                    plugins=self.apispec_options["plugins"])

        return api_spec

    def start_spec(self) -> APISpec:
        api_spec: APISpec = APISpec(self.apispec_options["title"],
                                    self.apispec_options["version"],
                                    self.apispec_options["openapi_version"],
                                    info=self.apispec_options["info"],
                                    plugins=self.apispec_options["plugins"])

        return api_spec

    def build_path(self, api_spec: APISpec, path_url: str, http_verb: str, response_code: int, parameter_object: Union[Dict, Schema] = None, response_object: ResponseObjectInterface = None):
        param_schema = Schema.from_dict(fields=parameter_object, name='ParameterSchema')

        content_type = mimetypes.MimeTypes().types_map[1]['.txt']
        try:
            content_type = response_object.content_type()
        except AttributeError as ae:
            content_type = magic.from_buffer(str(response_object), mime=True)

        schema = response_object.__name__
        try:
            schema = response_object.to_schema()
        except AttributeError as ae:
            pass

        operations: Dict = {
            http_verb.lower(): {
                "responses": {
                    str(response_code): {
                        "description": responses[response_code],
                        "content": {
                            content_type: {
                                "schema": schema
                            }
                        }
                    }
                },
                "parameters": [
                    {"in": "query", "schema": param_schema}
                ]
            }
        }

        api_spec.path(
            path=path_url,
            operations=operations
        )
        yml = api_spec.to_yaml()
        # return api_spec
