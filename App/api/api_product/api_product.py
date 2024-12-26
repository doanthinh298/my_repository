from sanic import response
from sanic import Request
from App.database.mongodb.database_store import Database
from sanic import Blueprint
from sanic_ext import openapi, validate

from App.model.project import Product, Create_Product, Update_Product
from App.utils.logger_utils import get_logger

logger = get_logger("crud_api")
db = Database()
product = Blueprint('product', url_prefix='/product')



@product.post("/")
@openapi.body({"application/json":Create_Product.model_json_schema()})
@openapi.definition(
    summary="Create a new product",
    tag="Product"
)
@validate(json= Create_Product)
async def create_product(request,body:Create_Product):
    if not body:
        return response.json({"error": "Missing product data"}, status=400)

    name = body.name
    category = body.category
    price = body.price
    stock = body.stock

    print(name, category, price,stock)

    if not name or not category or not price:
        return response.json({"error": "Missing required fields (name, category, price)"}, status=400)

    new_product = {
        "name": name,
        "category": category,
        "price": price,
        'stock':stock
    }

    created_product = db.create_product(new_product)

    if created_product:
        return response.json({"message": "Product created successfully"}, status=201)

    return response.json({"error": "Failed to create product"}, status=500)


@product.put("/<product_id>")
@openapi.definition(
    summary="Update an existing product",
    tag="Product"
)
@validate(json=Product)
async def update_product(request, product_id):
    update_data = request.json
    result = db.update_product(product_id, update_data)
    if result.modified_count:
        return response.json({"message": "Product updated successfully"})
    return response.json({"error": "Product not found"}, status=404)


@product.delete("/<product_id>")
@openapi.definition(
    summary="Delete a product",
    tag="Product"
)
async def delete_product(request, product_id):
    result = db.delete_product(product_id)
    if result.deleted_count:
        return response.json({"message": "Product deleted successfully"})
    return response.json({"error": "Product not found"}, status=404)

@product.get("/<product_id>")
@openapi.definition(
    summary="Get a product",
    tag="Product"
)
async def get_product(request, product_id):
    product_data = db.read_product(product_id)
    if product_data:
        product_data["_id"] = str(product_data["_id"])
        return response.json(product_data)
    return response.json({"error": "Product not found"}, status=404)

