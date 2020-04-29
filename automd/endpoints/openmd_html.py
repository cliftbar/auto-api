from typing import Dict

from apispec import APISpec
from flask import current_app, Response
from flask_restful import Resource

from automd.decorators import automd
from automd.automd import AutoMD
from automd.templates.openapi import generate_template_from_dict


class OpenMDHTML(Resource):
    @automd(summary='OpenAPI HTML Documentation Endpoint',
            description='Returns the OpenAPI HTML',
            tags=[{"name": "AutoMD"}])
    def get(self) -> str:
        auto_app: AutoMD = current_app.config[AutoMD.config_key].auto_md

        automd_spec: APISpec = auto_app.application_to_apispec(current_app)

        ret: Dict = automd_spec.to_dict()

        return Response(generate_template_from_dict(ret), mimetype='text/html')