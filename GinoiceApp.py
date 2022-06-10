import json
import re

from flask import Flask, redirect
from flask_swagger_ui import get_swaggerui_blueprint
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

from Models import *

app = Flask(__name__)

SWAGGER_URL = '/docs'
API_URL = '/swagger.json'
SWAGGER_UI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "GinoiceTestApp"
    }
)

app.register_blueprint(SWAGGER_UI_BLUEPRINT, url_prefix=SWAGGER_URL)

spec = APISpec(
    title='GinoiceTestApp',
    version='1.0.0',
    openapi_version='3.0.2',
    plugins=[FlaskPlugin(), MarshmallowPlugin()]
)

bearer_scheme = {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
spec.components.security_scheme("bearerAuth", bearer_scheme)

app.config.update({
    'APISPEC_SPEC': spec,
    'APISPEC_SWAGGER_URL': API_URL,
})
app.template_folder = "./static"


@app.route('/sign_up', methods=['POST'])
def registration(**kwargs):
    """
    ---
    post:
        summary: Registration
        description: Registration new user
        responses:
            200:
                description: Return id and signature
                content:
                    application/json:
                        schema: SignatureSchema
            400:
                description: Bad request
                content:
                    application/json:
                        schema: ErrorSchema
            401:
                description: Wrong email or password
                content:
                    application/json:
                        schema: ErrorSchema
            5XX:
                description: Unexpected Error
                content:
                    application/json:
                        schema: ErrorSchema
        requestBody:
            content:
                application/json:
                    schema: RegisterRequestSchema
    """

    return {"user_id": 1, "signature": "Some"}


@app.route('/sign_in', methods=['POST'])
def login():
    """
    ---
    post:
        summary: Login
        description: Get token for authentication
        responses:
            200:
                description: Return id and signature
                content:
                    application/json:
                        schema: AuthTokenSchema
            400:
                description: Bad request
                content:
                    application/json:
                        schema: ErrorSchema
            401:
                description: Wrong email or password
                content:
                    application/json:
                        schema: ErrorSchema
            5XX:
                description: Unexpected Error
                content:
                    application/json:
                        schema: ErrorSchema
        requestBody:
            content:
                application/json:
                    schema: LoginRequestSchema
    """
    pass
    return "login"


@app.route('/user', methods=['GET'])
def user():
    """
    ---
    get:
        summary: Get info
        description: Get info about logged user
        security:
            bearerAuth: []
        responses:
            200:
                description: Return id and signature
                content:
                    application/json:
                        schema: UserSchema
            401:
                description: You should have logged in
                content:
                    application/json:
                        schema: ErrorSchema
            5XX:
                description: Unexpected Error
                content:
                    application/json:
                        schema: ErrorSchema
    """
    pass
    return "user"


with app.test_request_context():
    spec.path(view=registration)
    spec.path(view=login)
    spec.path(view=user)


@app.route('/')
def default():
    return redirect(SWAGGER_URL)


@app.route("/swagger.json")
def swagger():
    file = json.dumps(spec.to_dict(), indent=2)
    fixed_file = re.sub(r"{\s*\"bearerAuth\":\s*\[\]\s*\}", "[{\n\"bearerAuth\": []\n}]", file)
    return fixed_file


if __name__ == "__main__":
    app.run(debug=True, port=5000)
