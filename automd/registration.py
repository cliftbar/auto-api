from enum import Enum
from typing import Dict, List

from flask_restful import Api

from automd.automd import AutoMD
from automd.encoder import AutoMDObjEncoder
from automd.endpoints.openmd_html import OpenMDHTML
from automd.endpoints.openmd_spec import OpenAPISpecJSON, OpenAPISpecYAML


class AutoMDSpecRoute(Enum):
    html = "html"
    json = "json"
    yml = "yml"
    yaml = "yaml"


class AutoMDApp:
    def __init__(self,
                 app_api: Api,
                 title: str,
                 app_version: str = "1.0.0",
                 openapi_version: str = "3.0.0",
                 info: Dict = None,
                 default_tag: str = None,
                 path_override: str = None,
                 spec_routes: List[AutoMDSpecRoute] = None):
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
                              Defaults to "/automd" (note leading, not trailing '/')
                              # TODO better path handling that string
        :param spec_routes: List containing routes to register, defaults to all.  List is made of
                            AutoMDSpecRoute enums
        """
        self.app_api: Api = app_api
        self.app_api.app.config[AutoMD.config_key] = self
        self.app_api.app.config["RESTFUL_JSON"] = {"cls": AutoMDObjEncoder}

        self.auto_md: AutoMD = AutoMD(title=title,
                                      app_version=app_version,
                                      openapi_version=openapi_version,
                                      info=info,
                                      default_tag=default_tag)

        endpoint_prefix: str = "automd"
        url: str = f"/{endpoint_prefix}" if path_override is None else path_override

        if spec_routes is None or AutoMDSpecRoute.json in spec_routes:
            app_api.add_resource(OpenAPISpecJSON, f"{url}/spec/json", endpoint=f"OpenAPISpecJSON_{endpoint_prefix}")
        if spec_routes is None or AutoMDSpecRoute.yaml in spec_routes:
            app_api.add_resource(OpenAPISpecYAML, f"{url}/spec/yaml", endpoint=f"OpenAPISpecYAML_{endpoint_prefix}")
        if spec_routes is None or AutoMDSpecRoute.yml in spec_routes:
            app_api.add_resource(OpenAPISpecYAML, f"{url}/spec/yml", endpoint=f"OpenAPISpecYML_{endpoint_prefix}")
        if spec_routes is None or AutoMDSpecRoute.html in spec_routes:
            app_api.add_resource(OpenMDHTML, f"{url}/html", endpoint=f"OpenAPIHTML_{endpoint_prefix}")
