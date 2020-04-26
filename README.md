# AutoAPI
AutoAPI is a documentation library for Flask APIs build with FlaskRESTful and Webargs.
Endpoint parameters and basic responses are automatically parsed into the OpenAPI specification,
using Type Hints and introspection, and a endpoints registered to serve the specification.

## Motivation
Documentation libraries tend to rely heavily on elaborate docstrings and static generation from source code.
This library requires minimal changes to existing code, and most information (especially parameter specs)
doesn't rely on keeping disparate strings up to date.  

## Usage
### AutoAPI registration/initialization
The first step is to initialize the AutoAPI app from a FlaskRESTful Api.

```python
app: Flask = Flask(__name__)
api: Api = Api(app)

spec: AutoAPIApp = AutoAPIApp(api, "AutoAPI Test App", "1.0.0", "3.0.0")
``` 

After that, all that is *required* is adding the `@autodoc` decorator to an existing Resource endpoint.

```python
class Status(Resource):
    get_query_arguments = {
        "text": fields.String(required=False)
    }

    @autodoc() # add new decorator
    @use_kwargs(get_query_arguments)
    def get(self, text=None):
        ret_text: str = "status check OK"
        if text is not None:
            ret_text = f"{text}: {text or 'Hello AutoAPI'}"

        return ret_text
```

which will mark the endpoint for inclusion in the OpenAPI spec.  In this example, the spec information
will be pretty limited, but will still have the API url, argument, and a default value.

More information can be provided in the webargs fields, autodoc tag, and use_kwargs tag,
as well has gleaned from better type hinting

```python
class Status(Resource):
    get_query_arguments = {
        "text": fields.String(required=False, description='Text to return', doc_default="Hello AutoAPI")
    }

    @autodoc(parameter_schema=get_query_arguments,
             summary="Status Endpoint",
             description="Status Endpoint, responds with a message made from the input string")
    @use_kwargs(get_query_arguments, location="query")
    def get(self, text: str = None) -> str:
        log_text: str = "status check OK"

        log_text = f"{log_text}: {text or 'Hello AutoAPI'}"

        return str(log_text)
```

With this information, argument types, return types, summaries, descriptions, detailed default
information, and parameter location info (body, query, etc) is included.  Summary and description
are the only "magic strings" needed, and those will generally not change much or be onerous to
keep up to date compared to the automatically grabbed information.

An example Flask API app is provided to showcase some functionality.  Start it using `run.py`.