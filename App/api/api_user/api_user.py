from sanic import  response
from App.database.mongodb.database_store import Database
from sanic import Blueprint
from sanic_ext import openapi, validate
from sanic import Request

from App.model.User import User
from App.utils.bcrypt import register_hash_password, check_password, hash_password
from App.model.project import Login_User,Register_User
from App.utils.jwt import generate_token, jwt_required
from App.utils.logger_utils import get_logger


logger = get_logger("crud_api")
db = Database()
user = Blueprint('user', url_prefix='/user')

# @user.post("/user")
# @openapi.definition(
#     summary="Create a new user",
#     tag="User Management"
# )
# @validate(json=User)
# async def create_user(request):
#     user_data = request.json
#     user_id = db.create_user(user_data)
#     return response.json({"user_id": str(user_id)})

# @user.put("/user/<user_id>")
# @openapi.definition(
#     summary="Update user information",
#     tag="User Management"
# )
# @validate(json=User)
# async def update_user(request, user_id):
#     update_data = request.json
#     result = db.update_user(user_id, update_data)
#     if result.modified_count:
#         return response.json({"message": "User updated successfully"})
#     return response.json({"error": "User not found"}, status=404)



@user.get("/user/get/<user_id>")
@openapi.definition(
    summary="Get a user",
    tag="User Management"
)
async def get_user(request, user_id):
    user_data = db.read_user(user_id)
    if user_data:
        user_data["_id"] = str(user_data["_id"])
        return response.json(user_data)
    return response.json({"error": "User not found"}, status=404)

@user.delete("/user/delete/<user_id>")
@openapi.definition(
    summary="Delete a user",
    tag="User Management"
)
async def delete_user(request, user_id):
    result = db.delete_user(user_id)
    if result.deleted_count:
        return response.json({"message": "User deleted successfully"})
    return response.json({"error": "User not found"}, status=404)


@user.post('/register')
@openapi.body({"application/json":Register_User.model_json_schema()})
@openapi.definition(
    summary="Retrieve a user's details",
    tag="User Management"
)
@validate(json = Register_User)
async def register(request, body: Register_User):
    if not body :
        return response.json({"error": "Missing product data"}, status=400)

    name = body.name
    email = body.email
    password = body.password
    address = body.address
    phone = body.phone

    existing_email = db.find_by_email(email)
    if existing_email:
        return response.json({"error": "Email đã tồn tại"}, status=400)

    existing_user = db.find_by_user(name)
    if existing_user:
        return response.json({"error": "Username đã tồn tại"}, status=400)

    hashed_password = hash_password(password)

    user_data = {
        "name": name,
        "email": email,
        "password": hashed_password,
        "address": address,
        "phone": phone
    }

    create_user = db.create_user(user_data)
    if create_user:
        return response.json({"message": "User registered successfully"}, status=201)
    return response.json({"error": "Failed to create product"}, status=500)


@user.post('/login')
@openapi.body({"application/json":Login_User.model_json_schema()})
@openapi.definition(
    summary="Retrieve a user's details",
    tag="User Management"
)
@validate(json = Login_User)
async def login(request, body: Login_User):
    if not body:
        return response.json({"error": "Missing product data"}, status=400)

    name = body.name
    password = body.password

    user = db.find_by_user(name)

    if not user:
        return response.json({"error": "Invalid name or password"}, status=401)

    if not check_password(password, user['password']):
        return response.json({"error": "Invalid name or password"}, status=401)

    token = generate_token(user['_id'])

    return response.json({"token": token}, status=200)