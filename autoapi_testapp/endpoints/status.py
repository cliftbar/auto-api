import logging
from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_kwargs, parser

from autoapi.decorators import autodoc
from autoapi.responses import ValueResponse, JSONResponse


class Status(Resource):
    get_query_arguments = {
        "text": fields.String(required=False, description='Text to return', doc_default="Hello AutoAPI")
    }

    @autodoc(parameter_schema=get_query_arguments,
             summary="Status Endpoint",
             description="Status Endpoint, logs a message and responds")
    @use_kwargs(get_query_arguments, location="query")
    def get(self, text: str = None) -> ValueResponse:
        log_text: str = "status check OK"

        if text is not None:
            log_text = f"{log_text}: {text or 'Hello AutoAPI'}"

        return ValueResponse(log_text)

    post_query_arguments = {
        "text": fields.String(required=False, description='Text to return', doc_default="Hello AutoAPI")
    }

    post_json_arguments = {
        "json_text": fields.String(description="Text to return (overrides query parameters)",
                                   doc_default="Hello AutoAPI")
    }

    @autodoc(parameter_schema={**post_query_arguments, **post_json_arguments},
             summary="Status Posting",
             description="Status Endpoint using post, responds with a message.  Json text overrides query text.")
    @use_kwargs(post_json_arguments, location="json")
    @use_kwargs(post_query_arguments, location="query")
    def post(self, text: str = None, json_text: str = None) -> JSONResponse:
        log_text: str = "status check OK"

        if text is not None:
            log_text = f"{log_text}: {json_text or text or 'Hello AutoAPI'}"

        return JSONResponse({"response": log_text})
