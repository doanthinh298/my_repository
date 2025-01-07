from datetime import datetime
from sanic import Sanic, response, json, Request, SanicException
from sanic import Blueprint
from sanic_ext import openapi, validate
from App.database.mongodb.database_store import Database
from App.model.project import Order
from App.utils.logger_utils import get_logger

logger = get_logger("crud_api_order")
db = Database()
order = Blueprint('order', url_prefix='/orders')

@order.post("/api/order")
@openapi.body({"application/json": Order.model_json_schema()})
@openapi.definition(
    summary="Create a new order",
    description="Create a new order and store it in the database, updating stock.",
    tag="Order Management"
)
@validate(json=Order)
async def place_order(request):
    try:
        data = request.json

        if 'user_id' not in data or 'products' not in data or 'total_price' not in data or 'shipping_address' not in data:
            raise SanicException("Dữ liệu thiếu", status_code=400)

        user_id = data['user_id']
        products = data['products']
        total_price = data['total_price']
        shipping_address = data['shipping_address']

        cart_items = await db.read_cart({"user_id": user_id})
        if not cart_items:
            raise SanicException("Giỏ hàng trống", status_code=400)

        order_data = {
            "user_id": user_id,
            "products": products,
            "total_price": total_price,
            "shipping_address": shipping_address,
            "status": "Đang xử lý",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        result = await db.create_order(order_data)

        for product in products:
            await db.update_product(
                {"_id": product['product_id']},
                {"$inc": {"stock": -product['quantity']}}
            )

        return response.json({
            "message": "Đặt hàng thành công!",
            "order": {
                "order_id": str(result.inserted_id),
                "user_id": user_id,
                "products": products,
                "total_price": total_price,
                "shipping_address": shipping_address,
                "status": "Đang xử lý",
                "created_at": order_data["created_at"],
                "updated_at": order_data["updated_at"]
            }
        }, status=201)

    except SanicException as se:
        return response.json({"error": str(se)}, status=se.status_code)

    except Exception as e:
        logger.error(f"Error in place_order: {str(e)}")
        return response.json({"error": str(e)}, status=500)


@order.get("/<order_id>")
@openapi.definition(
    summary="Get an order",
    description="Retrieve the details of an order using the order ID.",
    tag="Order Management"
)
async def get_order(request: Request, order_id: str):
    try:
        order = await db.read_order(order_id)
        if order:
            order["_id"] = str(order["_id"])
            return json(order)
        else:
            return json({"message": "Order not found"}, status=404)
    except Exception as e:
        logger.error(f"Error in get_order: {str(e)}")
        return json({"error": str(e)}, status=500)


@order.put("/<order_id>")
@openapi.definition(
    summary="Update an existing order",
    description="Update the status of an existing order.",
    tag="Order Management"
)
async def update_order_status(request: Request, order_id: str):
    try:
        data = request.json
        status = data.get("status")

        result = await db.update_order(
            order_id,
            {"$set": {
                "status": status,
                "updated_at": datetime.utcnow()
            }}
        )

        if result.modified_count > 0:
            order = await db.read_order(order_id)
            order["_id"] = str(order["_id"])
            return json(order)
        else:
            return json({"message": "Order not found or status is unchanged"}, status=404)
    except Exception as e:
        logger.error(f"Error in update_order_status: {str(e)}")
        return json({"error": str(e)}, status=500)


@order.delete("/<order_id>")
@openapi.definition(
    summary="Delete an order",
    description="Delete an order from the system using the order ID.",
    tag="Order Management"
)
async def delete_order(request: Request, order_id: str):
    try:
        result = await db.delete_order(order_id)

        if result.deleted_count > 0:
            return json({"message": "Order deleted successfully"})
        else:
            return json({"message": "Order not found"}, status=404)
    except Exception as e:
        logger.error(f"Error in delete_order: {str(e)}")
        return json({"error": str(e)}, status=500)
