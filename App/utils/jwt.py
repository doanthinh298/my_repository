from functools import wraps

from sanic.response import json
import jwt
from sanic.exceptions import Unauthorized


SECRET_KEY = "my_key"


def generate_token(user_id):

    payload = {
        "user_id": str(user_id)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def jwt_required():
    def decorator(f):
        @wraps(f)
        async def decorator_function(request, *args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                raise Unauthorized("Missing Authorization Header")

            try:
                user_data = decode_token(token)
                user_id = user_data['user_id']
            except Exception as e:
                raise Unauthorized("Invalid or expired token")

            request.headers['userId'] = user_id
            return await f(request, *args, **kwargs)

        return decorator_function
    return decorator


def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise Unauthorized("Token has expired")
    except jwt.InvalidTokenError:
        raise Unauthorized("Invalid token")


