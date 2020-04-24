from flask import Flask
from flask_restful import Api

from autoapi.registration import AutoAPIApp
from autoapi_testapp.endpoints import Status, AddTwo

# Initialize Flask App and API interface
app = Flask(__name__)
api = Api(app)

spec = AutoAPIApp(api, 'AutoAPI Test App', '1.0.0', "3.0.0")

# Disable 404 route suggestion from flask_restful
# It would append url suggestions to the error message on 404s, which is undesired behavior
app.config['ERROR_404_HELP'] = False


endpoint_prefix = 'status'
api.add_resource(Status, f'/{endpoint_prefix}/status', endpoint=f"Status_{endpoint_prefix}")
api.add_resource(AddTwo, f'/{endpoint_prefix}/add', endpoint=f"AddTwo_{endpoint_prefix}")
