import flask
from flask import Flask, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

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


@app.route('/')
def default():
    return flask.redirect('/docs')


@app.route(API_URL)
def create_swagger_spec():
    return jsonify(spec.to_dict())


@app.route('/sing_up')
def registration():
    pass
    return "registration"


@app.route('/sing_in')
def login():
    pass
    return "login"


@app.route('/user')
def user():
    pass
    return "user"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
