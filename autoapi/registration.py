from typing import Dict

from flask_restful import Api

from autoapi.autoapi import AutoAPI
from autoapi.endpoints.openapi_html import OpenAPIHTML
from autoapi.endpoints.openapi_spec import OpenAPISpec


def app_registration(app_api: Api, title, version, openapi_version, info: Dict = None, path_override: str = None):
    spec = AutoAPI(app_api, title, version, openapi_version, info)

    endpoint_prefix = 'autoapi'
    url = f'/{endpoint_prefix}/openapi' if path_override is None else path_override
    app_api.add_resource(OpenAPISpec, f"{url}/spec", endpoint=f"OpenAPISpec_{endpoint_prefix}")
    app_api.add_resource(OpenAPIHTML, f"{url}/html", endpoint=f"OpenAPIHTML_{endpoint_prefix}")

    return spec
