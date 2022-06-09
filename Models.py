from marshmallow import Schema, fields


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