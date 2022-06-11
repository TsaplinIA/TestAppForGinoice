import datetime
import jwt
import Config

from Database import User


def create_token(id, lifetime_minutes=30):
    expire = datetime.datetime.utcnow() + datetime.timedelta(
        minutes=lifetime_minutes)
    token = jwt.encode(
        {"user_id": id, "exp": expire},
        Config.APP_SECRET_KEY,
        algorithm="HS256"
    )
    if isinstance(token, bytes):
        token = token.decode()
    current_user: User = User.get(User.id == id)
    current_user.auth_token = token
    return token


def check_token(token):
    try:
        jwt_dict = jwt.decode(
            token,
            Config.APP_SECRET_KEY,
            algorithms=["HS256"]
        )
        user_id = jwt_dict["user_id"]
        expire = jwt_dict["exp"]

        user = User.get_or_none(User.id == user_id)
        if not user:
            return None

        return user_id
    except jwt.InvalidTokenError:
        return None
