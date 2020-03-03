import logging
from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_kwargs

from autoapi.decorators import introspection
from autoapi.responses import ValueResponse

logger = logging.getLogger(__name__)


class TextReturn(Resource):
    get_arguments = {
        "text": fields.String(required=False, description='Extra TextReturn', component_id="Text_id"),
        "log_text": fields.String(required=False, description='Extra log_text', component_id="log_text")
    }

    # @introspection(get_arguments, summary='Status Endpoint', description='Status Endpoint, logs a message and responds')
    @use_kwargs(get_arguments)
    def get(self, text: str = None) -> str:
        log_text: str = "status check OK"
        if text is not None:
            log_text = f"{log_text}: {text}"
        logger.info(log_text)

        return log_text
