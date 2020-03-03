from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from autoapi.registration import app_registration
from autoapi_testapp.endpoints import Status, TextReturn

# Initialize Flask App and API interface
app = Flask(__name__)
api = Api(app)

spec = app_registration(api, 'title', '1.0.0', "3.0.0")

CORS(app, resources={r"/*": {"origins": "*"}, r"/*": {"origins": "*"}}, supports_credentials=True)

# Disable 404 route suggestion from flask_restful
# It would append url suggestions to the error message on 404s, which is undesired behavior
app.config['ERROR_404_HELP'] = False


endpoint_prefix = 'status'
api.add_resource(Status, f'/{endpoint_prefix}', endpoint=f"Status_{endpoint_prefix}")
api.add_resource(TextReturn, f'/{endpoint_prefix}/text', endpoint=f"Text_{endpoint_prefix}")
