from sanic import Sanic, response
from App.database.mongodb.database_store import Database
from sanic import Blueprint
from sanic_ext import openapi, validate

from App.model.project import Order
from App.utils.logger_utils import get_logger

logger = get_logger("crud_api")
db = Database()
order = Blueprint('order', url_prefix='/order')


@order.get("/order/<order_id>")
@openapi.definition(
    summary="Retrieve an order's details",
    tag="Order Management"
)
async def get_order(request, order_id):
    order_data = db.read_order(order_id)
    if order_data:
        return response.json(order_data)
    return response.json({"error": "Order not found"}, status=404)


@order.put("/order/<order_id>")
@openapi.definition(
    summary="Update an existing order",
    tag="Order Management"
)
@validate(json=Order)
async def update_order(request, order_id):
    update_data = request.json
    result = db.update_order(order_id, update_data)
    if result.modified_count:
        return response.json({"message": "Order updated successfully"})
    return response.json({"error": "Order not found"}, status=404)


@order.delete("/order/<order_id>")
@openapi.definition(
    summary="Delete an order",
    tag="Order Management"
)
async def delete_order(request, order_id):
    result = db.delete_order(order_id)
    if result.deleted_count:
        return response.json({"message": "Order deleted successfully"})
    return response.json({"error": "Order not found"}, status=404)
