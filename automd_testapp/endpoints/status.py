from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_kwargs

from automd.decorators import automd
from automd.responses import ValueResponse, JSONResponse


class Status(Resource):
    get_query_arguments = {
        "text": fields.String(required=False, description='Text to return', doc_default="Hello AutoMD")
    }

    @automd(parameter_schema=get_query_arguments,
            summary="Status Endpoint",
            description="Status Endpoint, responds with a message made from the input string")
    @use_kwargs(get_query_arguments, location="query")
    def get(self, text: str = None) -> ValueResponse:
        ret_text: str = "status check OK"

        if text is not None:
            ret_text = f"{ret_text}: {text or 'Hello AutoMD'}"

        return ValueResponse(ret_text)

    post_query_arguments = {
        "text": fields.String(required=False, description='Text to return', doc_default="Hello AutoMD")
    }

    post_json_arguments = {
        "json_text": fields.String(description="Text to return (overrides query parameters)",
                                   doc_default="Hello AutoMD")
    }

    @automd(parameter_schema={**post_query_arguments, **post_json_arguments},
            summary="Status Posting",
            description="Status Endpoint using post, responds with a message.  Json text overrides query text.")
    @use_kwargs(post_json_arguments, location="json")
    @use_kwargs(post_query_arguments, location="query")
    def post(self, text: str = None, json_text: str = None) -> JSONResponse:
        ret_text: str = "status check OK"

        if text is not None:
            ret_text = f"{ret_text}: {json_text or text or 'Hello AutoMD'}"

        return JSONResponse({"response": ret_text})


class MinimalStatus(Resource):
    get_query_arguments = {
        "text": fields.String(required=False)
    }

    @automd()
    @use_kwargs(get_query_arguments)
    def get(self, text):
        return text


class IntrospectionStatus(Resource):
    post_query_arguments = {
        "text": fields.String(required=False)
    }

    @automd()
    @use_kwargs(post_query_arguments, location="json")
    def post(self, text: str = "Hello AutoMD") -> str:
        ret_text: str = "status check OK"

        if text is not None:
            ret_text = f"{ret_text}: {text}"

        return ret_text
