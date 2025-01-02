from datetime import datetime

from bson import ObjectId
from sanic import Sanic, response, json, Request
from sanic import Blueprint
from sanic_ext import openapi, validate
from App.database.mongodb.database_store import Database
from App.model.project import Order
from App.utils.logger_utils import get_logger

logger = get_logger("crud_api")
db = Database()
order = Blueprint('order', url_prefix='/orders')

@order.post("/")
@openapi.body({"application/json": Order.model_json_schema()})
@openapi.definition(
    summary="Create a new order",
    description="Create a new order ",
    tag="Order Management"
)
@validate(json=Order)
async def create_order(request: Request):
    body = request.json
    user_id = body.get("user_id")
    items = body.get("items")
    total_price = body.get("total_price")
    status = body.get("status", "pending")

    order = {
        "user_id": user_id,
        "items": items,
        "total_price": total_price,
        "status": status,
        "created_at": datetime.now()
    }

    result = db.create_order(order)

    return json({
        "order_id": str(result.inserted_id),
        "status": status,
        "total_price": total_price,
        "items": items
    })


@order.get("/<order_id>")
@openapi.definition(
    summary="Get an order",
    description="Retrieve the details of an order using the order ID.",
    tag="Order Management"
)
async def get_order(request: Request, order_id: str):
    order = db.read_order(order_id)
    if order:
        order["_id"] = str(order["_id"])
        return json(order)
    else:
        return json({"message": "Order not found"}, status=404)


@order.put("/<order_id>")
@openapi.definition(
    summary="Update an existing order",
    description="Update the status of an existing order.",
    tag="Order Management"
)
async def update_order_status(request: Request, order_id: str):
    data = request.json
    status = data.get("status")

    result = db.update_order(
        order_id,
        {"$set": {"status": status, "updated_at": datetime.now()}}
    )

    if result.modified_count > 0:
        order = db.read_order(order_id)
        order["_id"] = str(order["_id"])
        return json(order)
    else:
        return json({"message": "Order not found or status is unchanged"}, status=404)


@order.delete("/<order_id>")
@openapi.definition(
    summary="Delete an order",
    description="Delete an order from the system using the order ID.",
    tag="Order Management"
)
async def delete_order(request: Request, order_id: str):
    result = db.delete_order(order_id)

    if result.deleted_count > 0:
        return json({"message": "Order deleted successfully"})
    else:
        return json({"message": "Order not found"}, status=404)