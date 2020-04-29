from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_kwargs

from automd.decorators import automd


class AddTwo(Resource):
    get_arguments = {
        "first_number": fields.Float(required=True, description="First Number to Add"),
        "second_number": fields.Float(required=True, description="Second Number to Add")
    }

    @automd(parameter_schema=get_arguments,
            summary='Add Endpoint',
            description='Returns the sum of two numbers.  Takes arguments in Query Parameters',
            tags=[{"name": "Math"}])
    @use_kwargs(get_arguments, location="query")
    def get(self, first_number: float, second_number: float) -> float:
        return first_number + second_number


class MultiplyTwo(Resource):
    get_arguments = {
        "first_number": fields.Float(required=True, description="First Number to Multiply"),
        "second_number": fields.Float(required=True, description="Second Number to Multiply")
    }

    @automd(parameter_schema=get_arguments,
            summary='Multiply Endpoint',
            description='Multiplies two numbers and returns the result.  Takes arguments in JSON',
            tags=[{"name": "Math"}])
    # TODO: Get accurate location, may have to implement our own use_kwargs
    @use_kwargs(get_arguments, location="json")
    def get(self, first_number: float, second_number: float) -> float:
        return first_number * second_number
