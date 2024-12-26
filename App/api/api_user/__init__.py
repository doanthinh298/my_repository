from sanic import Blueprint

from App.api.api_user.api_user import user


user_api = Blueprint.group(
    user
)

