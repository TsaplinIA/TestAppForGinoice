import re

from marshmallow import ValidationError
from flask import make_response
from web3.auto import w3
from eth_account.messages import defunct_hash_message
import Config


def check_correct_request(json, schema):
    try:
        schema().load(json)
    except ValidationError as error:
        print(error.messages)
        if error.messages.get("email")[0] == "Not a valid email address.":
            print(456)
            return make_response({"error": "Invalid email or password"}, 401)
        return make_response({"error": "Bad request"}, 400)

    return None


def check_correct_password(password):
    print(re.search(r"[A-Z]+", password))
    if not re.search(r"\d+", password) or not re.search(r"[A-Z]+", password) or len(password) < 8:
        print(123)
        return make_response({"error": "Invalid email or password"}, 401)
    return None



def get_signature(id: int):
    hash = w3.solidityKeccak(['uint256'], [id])
    ethHash = defunct_hash_message(hash)
    signed_message = w3.eth.account.signHash(ethHash, Config.ETH_PRIVATE_KEY)
    signature = signed_message.signature
    return signature.hex()




if __name__ == "__main__":
    print(get_signature(123))