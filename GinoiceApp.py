import json
import re

from flask import Flask, redirect, request, make_response
from flask_swagger_ui import get_swaggerui_blueprint
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

from Models import *
from MyTools import check_correct_request, register_new_user, my_login, get_user_info
from TokenTools import check_token

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
def registration():
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
                description: Invalid email or password
                content:
                    application/json:
                        schema: ErrorSchema
            410:
                description: User already registered
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
    request_json = request.json
    match(check_correct_request(request_json, RegisterRequestSchema)):
        case 400:
            return make_response({"error": "Bad request"}, 400)
        case 401:
            return make_response({"error": "Invalid email or password"}, 401)
        case _:
            pass

    register_json = register_new_user(request_json)
    error_message = register_json.get("error", None)
    if error_message:
        return make_response({"error": error_message}, 410)

    return make_response({"user_id": register_json["user_id"], "signature": register_json["user_sign"]}, 200)


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
                description: Invalid/Wrong email or password
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
    request_json = request.json
    match (check_correct_request(request_json, LoginRequestSchema)):
        case 400:
            return make_response({"error": "Bad request"}, 400)
        case 401:
            return make_response({"error": "Invalid email or password"}, 401)
        case _:
            pass
    token = my_login(request_json["email"], request_json["password"])
    if token:
        return make_response({"auth_token": token}, 200)
    return make_response({"error": "Wrong email or password"}, 401)


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
                description: You must have logged in
                content:
                    application/json:
                        schema: ErrorSchema
            403:
                description: Invalid token
                content:
                    application/json:
                        schema: ErrorSchema
            5XX:
                description: Unexpected Error
                content:
                    application/json:
                        schema: ErrorSchema
    """
    try:
        auth_header = request.headers.get('Authorization')
    except KeyError:
        return make_response({"error": "You must have logged in"}, 401)
    auth_token = re.sub(r"Bearer\s+", "", auth_header)
    user_id = check_token(auth_token)
    if user_id:
        return make_response(get_user_info(user_id), 200)

    return make_response({"message": "Invalid token"}, 403)


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


@app.errorhandler(400)
def bad_request(_):
    return make_response({"error": "Bad request"}, 400)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
