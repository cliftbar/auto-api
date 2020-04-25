import logging

from typing import Dict

from apispec import APISpec
from flask import current_app
from flask_restful import Resource

from autoapi.decorators import autodoc
from autoapi.autoapi import AutoAPI

logger = logging.getLogger(__name__)


class OpenAPISpecJSON(Resource):
    @autodoc(summary="OpenAPI JSON Documentation Endpoint",
             description="Returns the OpenAPI Spec in JSON format",
             tags=[{"name": "AutoAPI"}])
    def get(self) -> Dict:
        auto_app: AutoAPI = current_app.config[AutoAPI.config_key].auto_api

        autoapi_spec: APISpec = auto_app.application_to_apispec(current_app)

        ret: Dict = autoapi_spec.to_dict()

        return ret


class OpenAPISpecYAML(Resource):
    @autodoc(summary="OpenAPI Yaml Documentation Endpoint",
             description="Returns the OpenAPI Spec in Yaml format",
             tags=[{"name": "AutoAPI"}])
    def get(self) -> str:
        auto_app: AutoAPI = current_app.config[AutoAPI.config_key].auto_api

        autoapi_spec: APISpec = auto_app.application_to_apispec(current_app)

        ret: str = autoapi_spec.to_yaml()

        return ret
