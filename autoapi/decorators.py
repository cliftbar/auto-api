from typing import Callable, Dict, List

from autoapi.autoapi import AutoAPI


def autodoc(parameter_schema: Dict = None,
            summary: str = None,
            description: str = None,
            tags: List[Dict] = None) -> Callable:
    """
    Decorator to perform documentation introspection on a FlaskRESTful Resource Class.
    Place before any FlaskRESTful argument parsers.
    :param parameter_schema: same as get passed into use_kwargs
    :param summary: Quick overview of the endpoint
    :param description: Detailed information about the endpoint
    :param tags: Controls which section the documentation is shown in
    :return:
    """
    if parameter_schema is None:
        parameter_schema = {}

    def autodoc_wrapper(func: Callable) -> Callable:
        return_type = func.__annotations__.get("return")

        autoapi_spec_parameters = {}

        if summary is not None:
            autoapi_spec_parameters["summary"] = summary

        if description is not None:
            autoapi_spec_parameters["description"] = description

        if tags is not None:
            autoapi_spec_parameters["tags"] = tags

        autoapi_spec_parameters["parameter_schema"] = parameter_schema

        autoapi_spec_parameters["response_schemas"] = {
            "200": return_type
        }

        setattr(func, AutoAPI.function_key, autoapi_spec_parameters)

        return func
    return autodoc_wrapper
