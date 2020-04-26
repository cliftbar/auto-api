from enum import Enum
from typing import Dict, List

from flask_restful import Api

from autoapi.autoapi import AutoAPI
from autoapi.encoder import AutoAPIObjEncoder
from autoapi.endpoints.openapi_html import OpenAPIHTML
from autoapi.endpoints.openapi_spec import OpenAPISpecJSON, OpenAPISpecYAML


class AutoAPISpecRoute(Enum):
    html = "html"
    json = "json"
    yml = "yml"
    yaml = "yaml"


class AutoAPIApp:
    def __init__(self,
                 app_api: Api,
                 title: str,
                 app_version: str = "1.0.0",
                 openapi_version: str = "3.0.0",
                 info: Dict = None,
                 default_tag: str = None,
                 path_override: str = None,
                 spec_routes: List[AutoAPISpecRoute] = None):
        """
        Configures OpenAPI documentation generator for the FlaskRESTful application.
        Also extends flask.json.JSONEncoder in the application config key "RESTFUL_JSON".
        :param app_api: FlaskRESTful API app to instantiate the documentation for.
        :param title: Application title
        :param app_version: Application version
        :param openapi_version: OpenAPI spec version presented.
        :param info: Detailed information about the application.
        :param default_tag: Tag to apply to endpoints if not specified in their decorator.
        :param path_override: Replaces the base path of the documentation routes.
                              Defaults to "/autoapi" (note leading, not trailing '/')
                              # TODO better path handling that string
        :param spec_routes: List containing routes to register, defaults to all.  List is made of
                            AutoAPISpecRoute enums
        """
        self.app_api: Api = app_api
        self.app_api.app.config[AutoAPI.config_key] = self
        self.app_api.app.config["RESTFUL_JSON"] = {"cls": AutoAPIObjEncoder}

        self.auto_api: AutoAPI = AutoAPI(title=title,
                                         app_version=app_version,
                                         openapi_version=openapi_version,
                                         info=info,
                                         default_tag=default_tag)

        endpoint_prefix: str = "autoapi"
        url: str = f"/{endpoint_prefix}" if path_override is None else path_override

        # if spec_routes is None or AutoAPISpecRoute.json in spec_routes:
        #     app_api.add_resource(OpenAPISpecJSON, f"{url}/spec/json", endpoint=f"OpenAPISpecJSON_{endpoint_prefix}")
        # if spec_routes is None or AutoAPISpecRoute.yaml in spec_routes:
        #     app_api.add_resource(OpenAPISpecYAML, f"{url}/spec/yaml", endpoint=f"OpenAPISpecYAML_{endpoint_prefix}")
        # if spec_routes is None or AutoAPISpecRoute.yml in spec_routes:
        #     app_api.add_resource(OpenAPISpecYAML, f"{url}/spec/yml", endpoint=f"OpenAPISpecYML_{endpoint_prefix}")
        if spec_routes is None or AutoAPISpecRoute.html in spec_routes:
            app_api.add_resource(OpenAPIHTML, f"{url}/html", endpoint=f"OpenAPIHTML_{endpoint_prefix}")
