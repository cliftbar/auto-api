from typing import Callable, Dict

from autoapi.autoapi import AutoAPI


def introspection(parameter_schema: Dict = None, summary: str = None, description: str = None):
    if parameter_schema is None:
        parameter_schema = {}

    def wrap_1(func: Callable):
        return_type = func.__annotations__.get('return')

        autoapi_spec_parameters = {}

        if summary is not None:
            autoapi_spec_parameters['summary'] = summary

        if description is not None:
            autoapi_spec_parameters['description'] = description

        autoapi_spec_parameters["parameter_schema"] = parameter_schema

        autoapi_spec_parameters['response_schemas'] = {
            "200": return_type
        }

        setattr(func, AutoAPI.function_key, autoapi_spec_parameters)

        return func
    return wrap_1
