import logging
from typing import Dict

from apispec import APISpec
from flask import current_app, Response
from flask import url_for

from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_kwargs

from autoapi.decorators import introspection
from autoapi.autoapi import AutoAPI
from autoapi.responses import ValueResponse
from autoapi.templates.openapi import generate_template_from_dict

logger = logging.getLogger(__name__)


class OpenAPIHTML(Resource):
    # @introspection(summary='OpenAPI HTML Documentation Endpoint', description='Returns the OpenAPI HTML')
    def get(self) -> str:
        autoapi: AutoAPI = current_app.config[AutoAPI.config_key]
        autoapi_spec: APISpec = autoapi.start_spec()

        endpoint: Resource
        for name, view in current_app.view_functions.items():
            if not hasattr(view, 'methods'):
                continue
            for method in view.methods:

                key = url_for(view.view_class.endpoint)  # f"{url_for(view.view_class.endpoint)}: {method}"
                value_func = getattr(view.view_class, method.lower())

                if hasattr(value_func, AutoAPI.function_key):
                    autoapi_spec_parameters = getattr(value_func, AutoAPI.function_key)
                    response_schemas = autoapi_spec_parameters.get("response_schemas")
                    parameter_schema = autoapi_spec_parameters.get("parameter_schema")
                    summary: str = autoapi_spec_parameters.get("summary")
                    description: str = autoapi_spec_parameters.get("description")
                    autoapi.build_path(autoapi_spec, key, method, 200, summary, description, parameter_schema, response_schemas["200"])

        ret: Dict = autoapi_spec.to_dict()

        return Response(generate_template_from_dict(ret), mimetype='text/html')
