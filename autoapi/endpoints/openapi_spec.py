import logging

from apispec import APISpec
from flask import current_app
from flask import url_for

from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_kwargs

from autoapi.decorators import introspection
from autoapi.autoapi import AutoAPI
from autoapi.responses import ValueResponse

logger = logging.getLogger(__name__)


class OpenAPISpec(Resource):
    get_arguments = {
        'response_type': fields.String(required=False, description="Format to return the OpenAPI spec as; yaml or json", doc_default='json')
    }

    @introspection(get_arguments, summary='OpenAPI Documentation Endpoint', description='Returns the OpenAPI Spec')
    @use_kwargs(get_arguments)
    def get(self, response_type: str = 'json') -> ValueResponse:
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
                    autoapi.build_path(autoapi_spec, key, method, 200, parameter_schema, response_schemas["200"])

        ret = autoapi_spec.to_dict()
        if response_type.lower() in ["yml", "yaml"]:
            ret = autoapi_spec.to_yaml()

        return ValueResponse(ret)
