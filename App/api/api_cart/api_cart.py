from sanic import Sanic, response, Blueprint
from sanic_ext import validate
from sanic_ext.extensions.openapi import openapi

from App.database.mongodb.database_store import Database
from App.model.project import AddToCartModel, GetCart
from App.utils.jwt import jwt_required
from App.utils.logger_utils import get_logger


logger = get_logger("crud_api")
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
@validate(json = AddToCartModel)
async def add_to_cart(request, body : AddToCartModel):
    if not body :
        return response.json({"error": "Missing product data"}, status=400)
    try:
        user_id = request.headers.get('userId')
        print(user_id)
        body = request.json

        product_id = body.get("product_id")
        quantity = body.get("quantity", 1)

        if not product_id:
            return response.json({"error": "product_id is required"}, status=400)

        update_query = {"user_id": user_id}

        update_cart= {
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

@cart.get("/cart/get")
@openapi.body({"application/json": GetCart.model_json_schema()})
@openapi.definition(
    summary="Get cart information",
    tag="Cart"
)
@openapi.secured('Authorization')
@jwt_required()
@validate(json = GetCart)
async def get_cart(request,body : GetCart):
    if not body:
        return response.json({"error": "Missing product data"}, status=400)
    try:
        user_id = request.headers.get('userId')
        if not user_id:
            return response.json({"error": "user_id is required in headers"}, status=400)

        cart = await db.read_cart({"user_id": user_id})
        if not cart:
            return response.json({"message": "Cart is empty"}, status=404)

        return response.json({"cart": cart}, status=200)
    except Exception as e:
        logger.error(f"Error in get_cart: {str(e)}")
        return response.json({"error": str(e)}, status=500)


@cart.put("/cart/update")
@openapi.body({"application/json": AddToCartModel.model_json_schema()})
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


@cart.delete("/cart/clear")
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


@cart.get("/cart/total")
@openapi.definition(
    summary="Get total amount of products in cart",
    tag="Cart"
)
@openapi.secured('Authorization')

@jwt_required()
async def get_cart_total(request):
    try:
        user_id = request.headers.get('userId')

        cart = db.read_cart(user_id)

        if not cart:
            return response.json({"message": "Cart not found for user"}, status=404)

        total_amount = 0
        for item in cart['items']:
            product = db.read_product(item['product_id'])
            if product:
                total_amount += product['price'] * item['quantity']
            else:
                logger.warning(f"Product with ID {item['product_id']} not found")

        return response.json({"total_amount": total_amount}, status=200)
    except Exception as e:
        logger.error(f"Error in get_cart_total: {str(e)}")
        return response.json({"error": str(e)}, status=500)
