from typing import Dict

from apispec import APISpec
from flask import current_app, Response
from flask_restful import Resource

from autoapi.decorators import autodoc
from autoapi.autoapi import AutoAPI
from autoapi.templates.openapi import generate_template_from_dict


class OpenAPIHTML(Resource):
    @autodoc(summary='OpenAPI HTML Documentation Endpoint',
             description='Returns the OpenAPI HTML',
             tags=[{"name": "AutoAPI"}])
    def get(self) -> str:
        auto_app: AutoAPI = current_app.config[AutoAPI.config_key].auto_api

        autoapi_spec: APISpec = auto_app.application_to_apispec(current_app)

        ret: Dict = autoapi_spec.to_dict()

        return Response(generate_template_from_dict(ret), mimetype='text/html')
