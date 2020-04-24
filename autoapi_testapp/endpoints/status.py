import logging
from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_kwargs

from autoapi.decorators import autodoc
from autoapi.responses import ValueResponse


class Status(Resource):
    get_arguments = {
        "text": fields.String(required=False, description='Text to return', doc_default="Hello AutoAPI")
    }

    @autodoc(parameter_schema=get_arguments,
             summary="Status Endpoint",
             description="Status Endpoint, logs a message and responds")
    @use_kwargs(get_arguments, location="query")
    def get(self, text: str = "Hello AutoAPI") -> ValueResponse:
        log_text: str = "status check OK"

        if text is not None:
            log_text = f"{log_text}: {text}"

        return ValueResponse(log_text)
