from flask import Flask
from flask_restful import Api
from webargs.flaskparser import parser, abort

from autoapi.registration import AutoAPIApp
from autoapi_testapp.endpoints import Status, AddTwo

# Initialize Flask App and API interface
from autoapi_testapp.endpoints.add_two import MultiplyTwo

app: Flask = Flask(__name__)
api: Api = Api(app)

spec: AutoAPIApp = AutoAPIApp(api, "AutoAPI Test App", "1.0.0", "3.0.0")

# Disable 404 route suggestion from flask_restful
# It would append url suggestions to the error message on 404s, which is undesired behavior
app.config["ERROR_404_HELP"] = False
@parser.error_handler
def handle_request_parsing_error(err, req, schema, *, error_status_code, error_headers):
    """webargs error handler that uses Flask-RESTful's abort function to return
    a JSON error response to the client.
    """
    abort(error_status_code, errors=err.messages)

endpoint_prefix: str = "status"
api.add_resource(Status, f"/{endpoint_prefix}/status", endpoint=f"Status_{endpoint_prefix}")
api.add_resource(AddTwo, f"/{endpoint_prefix}/add", endpoint=f"AddTwo_{endpoint_prefix}")
api.add_resource(MultiplyTwo, f"/{endpoint_prefix}/multiply", endpoint=f"MultiplyTwo_{endpoint_prefix}")
