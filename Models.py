from marshmallow import Schema, fields


class RegisterRequestSchema(Schema):
    name = fields.Str(required=True)
    surname = fields.Str(required=True)
    email = fields.Email(required=True)
    eth_address = fields.Str(required=True)
    password = fields.Str(required=True)


class ErrorSchema(Schema):
    error = fields.Str()

class SignatureSchema(Schema):
    user_id = fields.Int()
    signature = fields.Str()


class AuthTokenSchema(Schema):
    auth_token = fields.Str()


class UserSchema(Schema):
    name = fields.Str()
    surname = fields.Str()
    email = fields.Str()
    eth_address = fields.Str()