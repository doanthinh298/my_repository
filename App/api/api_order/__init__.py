from sanic import Blueprint

from App.api.api_order.api_order import order

order_api = Blueprint.group(
    order
)

