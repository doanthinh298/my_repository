from sanic import Blueprint

from App.api.api_product.api_product import product


product_api = Blueprint.group(
    product
)

