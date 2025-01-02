from sanic import Blueprint

from App.api.api_cart.api_cart import cart
from App.api.api_order.api_order import order
from App.api.api_product.api_product import product
from App.api.api_user.api_user import user


api = Blueprint.group(
    order,
    product,
    user,
    cart
    )