from sanic import Sanic, response, Blueprint
from sanic_ext import validate
from sanic_ext.extensions.openapi import openapi

from App.database.mongodb.database_store import Database
from App.model.project import AddToCartModel, GetCart, UpdateCartModel
from App.utils.jwt import jwt_required
from App.utils.logger_utils import get_logger


logger = get_logger("crud_api_cart")
db = Database()

cart = Blueprint('cart', url_prefix='/cart')


@cart.post("/cart/add")
@openapi.body({"application/json": AddToCartModel.model_json_schema()})
@openapi.definition(
    summary="Create or update a cart",
    tag="Cart"
)
@openapi.secured('Authorization')
@jwt_required()
@validate(json=AddToCartModel)
async def add_to_cart(request, body: AddToCartModel):
    if not body:
        return response.json({"error": "Missing product data"}, status=400)

    try:
        user_id = request.headers.get('userId')
        if not user_id:
            return response.json({"error": "Missing userId in headers"}, status=400)

        product_name = body.name
        quantity = body.quantity

        product = db.Product.find_one({"name": product_name})

        if not product:
            return response.json({"error": f"Product '{product_name}' not found"}, status=404)

        products = db.find_product_by_name({"name": product_name})
        if len(products) > 1:
            return response.json({"error": f"Multiple products found with name '{product_name}'. Please specify."},
                                 status=400)

        product_id = str(product["_id"])

        update_query = {"user_id": user_id}
        update_cart = {
            "$setOnInsert": {"user_id": user_id},
            "$push": {"items": {"product_id": product_id, "quantity": quantity}}
        }

        result = db.update_cart(update_query, update_cart)

        if result.matched_count == 0 and result.upserted_id:
            message = "Cart created and product added successfully"
        else:
            message = "Product added to cart successfully"

        return response.json({"message": message}, status=200)

    except Exception as e:
        logger.error(f"Error in add_to_cart: {str(e)}")
        return response.json({"error": str(e)}, status=500)


@cart.get("/cart/get/<user_id>")
@openapi.definition(
    summary="Get cart information",
    tag="Cart"
)
@openapi.secured('Authorization')
@jwt_required()
async def get_cart(request, user_id: str):

    try:
        if not user_id:
            return response.json({"error": "User ID is required"}, status=400)

        cart = db.read_cart(user_id)

        if not cart:
            return response.json({"message": "Cart not found for this user"}, status=404)

        return response.json({"cart": cart.to_dict() if hasattr(cart, 'to_dict') else cart}, status=200)

    except Exception as e:
        logger.error(f"Error in get_cart: {str(e)}")
        return response.json({"error": "Internal server error"}, status=500)

@cart.put("/cart/update")
@openapi.body({"application/json": UpdateCartModel.model_json_schema()})
@openapi.definition(
    summary="Update product quantity in cart",
    tag="Cart"
)
@jwt_required()
async def update_cart(request):
    try:
        user_id = request.user_id
        body = request.json

        product_id = body.get("product_id")
        quantity = body.get("quantity", 1)

        if not product_id:
            return response.json({"error": "product_id is required"}, status=400)

        update_query = {"user_id": user_id, "items.product_id": product_id}
        update_operation = {"$set": {"items.$.quantity": quantity}}

        result = db.update_cart(update_query, update_operation)

        if result.modified_count:
            return response.json({"message": "Product quantity updated successfully"}, status=200)
        return response.json({"error": "Product not found in cart"}, status=404)
    except Exception as e:
        logger.error(f"Error in update_cart: {str(e)}")
        return response.json({"error": str(e)}, status=500)

@cart.delete("/cart/clear/<user_id>")
@openapi.definition(
    summary="Clear all products in cart",
    tag="Cart"
)
@jwt_required()
async def clear_cart(request):
    try:
        user_id = request.headers.get('userId')

        result = db.delete_cart(user_id)

        if result.deleted_count:
            return response.json({"message": "Cart cleared successfully"}, status=200)
        return response.json({"error": "Cart not found for user"}, status=404)
    except Exception as e:
        logger.error(f"Error in clear_cart: {str(e)}")
        return response.json({"error": str(e)}, status=500)

