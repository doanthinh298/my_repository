# from sanic import Sanic, response
# from sanic_jwt import initialize, exceptions
#
# from App.api.api_product.api_product import db
#
# SECRET_KEY = "your_secret_key"
#
#
# async def retrieve_user(request, payload, *args, **kwargs):
#     if not payload:
#         raise exceptions.AuthenticationFailed("Token không hợp lệ")
#     return {
#         "user_id": payload.get("user_id"),
#         "email": payload.get("email"),
#         "name": payload.get("name")
#     }
#
#
# async def extend_payload(payload, user, *args, **kwargs):
#     payload.update({
#         "user_id": user.get("user_id"),
#         "email": user.get("email"),
#         "name": user.get("name")
#     })
#     return payload
#
#
# async def authenticate(request):
#     data = request.json
#     if not data or "email" not in data or "password" not in data:
#         raise exceptions.AuthenticationFailed("Email và mật khẩu là bắt buộc")
#
#     email = data.get("email")
#     password = data.get("password")
#     user = await db["Users"].find_one({"email": email, "password": password})
#
#     if not user:
#         raise exceptions.AuthenticationFailed("Email hoặc mật khẩu không chính xác")
#
#     return {
#         "user_id": str(user["_id"]),
#         "email": user["email"],
#         "name": user["name"]
#     }
#
#
# app = Sanic("AuthMiddleware")
# initialize(
#     app,
#     authenticate=authenticate,
#     retrieve_user=retrieve_user,
#     extend_payload=extend_payload,
#     secret=SECRET_KEY
# )
