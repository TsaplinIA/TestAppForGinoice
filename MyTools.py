import re

import bcrypt as bcrypt
from marshmallow import ValidationError
from flask import make_response
from web3.auto import w3
from eth_account.messages import defunct_hash_message
from peewee import IntegrityError

import Config
from Database import User
from TokenTools import create_token


def check_correct_request(json, schema):
    try:
        schema().load(json)
        if not check_correct_password(json["password"]):
            return 401
    except ValidationError as error:
        if error.messages.get("email")[0] == "Not a valid email address.":
            return 401
        else:
            return 400


def check_correct_password(password):
    if not re.search(r"\d+", password) or not re.search(r"[A-Z]+", password) or len(password) < 8:
        return False
    return True


def get_signature(id: int):
    hash = w3.solidityKeccak(['uint256'], [id])
    ethHash = defunct_hash_message(hash)
    signed_message = w3.eth.account.signHash(ethHash, Config.ETH_PRIVATE_KEY)
    signature = signed_message.signature
    return signature.hex()


def register_new_user(json):
    result = dict()
    try:
        user = User.create(
            name=json["name"],
            surname=json["surname"],
            email=json["email"],
            eth_address=json["eth_address"],
            password=bcrypt.hashpw(json["password"].encode(), bcrypt.gensalt()),
            auth_token="None"
        )
        result["user_id"] = user.id
        result["user_sign"] = get_signature(user.id)
    except IntegrityError as error:
        error_message: str = error.args[0]
        result["error"] = f"User with this {error_message.split('.')[-1]} already registered"

    return result


def my_login(email, password):
    user = User.get_or_none(User.email == email)
    if user:
        if bcrypt.checkpw(password.encode(), user.password):
            return create_token(user.id)
    return None


def get_user_info(id):
    user = User.get_or_none(User.id == id)
    if user:
        return {
            "name": user.name,
            "surname": user.surname,
            "email": user.email,
            "eth_address": user.eth_address,
        }
    return None
