from bson import ObjectId
from sanic import response, json, SanicException
from sanic import Request
from App.database.mongodb.database_store import Database
from sanic import Blueprint
from sanic_ext import openapi, validate

from App.model.project import Product, Create_Product, Update_Product
from App.utils.logger_utils import get_logger

logger = get_logger("crud_api_product")
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
    description = body.description

    if not name or not category or not price:
        return response.json({"error": "Missing required fields (name, category, price)"}, status=400)

    new_product = {
        "name": name,
        'description':description,
        "category": category,
        "price": price,
        'stock':stock,
    }

    created_product = db.create_product(new_product)

    if created_product:
        return response.json({"message": "Product created successfully"}, status=201)

    return response.json({"error": "Failed to create product"}, status=500)


@product.put("/<product_id>")
@openapi.body({"application/json": Update_Product.model_json_schema()})
@openapi.definition(
    summary="Update an existing product",
    tag="Product",
    description="Update the details of an existing product by providing the updated fields."
)
@validate(json=Update_Product)
async def update_product(request, product_id, body: Product):

    if not body:
        return response.json({"error": "Missing product data"}, status=400)

    update_data = {
        "name": body.name,
        "category": body.category,
        "price": body.price,
        "stock": body.stock,
        "description":body.description
    }

    result = db.update_product(product_id, update_data)

    if result.modified_count:
        return response.json({"message": "Product updated successfully"}, status=200)

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

@product.get("/")
@openapi.definition(
    summary="Get all products",
    tag="Product"
)
async def get_all_products(request):
    products_data = db.read_all_products()

    products = list(products_data)

    if products:
        for product in products:
            product["_id"] = str(product["_id"])

        return response.json(products)

    return response.json({"error": "No products found"}, status=404)


# Tìm kiếm sản phẩm
#
# @product.get("/api/products/search")
# async def search_products(request):
#     query = request.args.get('query', '').strip()
#     if not query:
#         return json({"error": "Yêu cầu tìm kiếm trống!"}, status=400)
#
#     try:
#         limit = max(1, int(request.args.get('limit', 10)))
#         skip = max(0, int(request.args.get('skip', 0)))
#
#         products_cursor = db.read_product(
#             {"$text": {"$search": query}},
#             {"_id": 1, "name": 1, "price": 1, "stock": 1}
#         )
#
#         products = products_cursor.skip(skip).limit(limit)
#
#         products_list = list(products)
#
#         return json({"products": products_list}, status=200)
#
#     except ValueError:
#         return json({"error": "Giá trị limit hoặc skip không hợp lệ!"}, status=400)
#
#     except Exception as e:
#         return json({"error": f"Lỗi không xác định: {str(e)}"}, status=500)
#
# # kiem tra ton kho
# @product.get("/api/product/stock/<product_id>")
# async def check_stock(request, product_id):
#     try:
#         product_id = ObjectId(product_id)
#     except Exception:
#         raise SanicException("ID sản phẩm không hợp lệ", status_code=400)
#
#     try:
#         product = db.read_product({"_id": product_id})
#     except Exception as e:
#         return json({"error": f"Lỗi khi truy vấn dữ liệu: {str(e)}"}, status=500)
#
#     if not product:
#         raise SanicException("Sản phẩm không tồn tại", status_code=404)
#
#     return json({
#         "product_id": str(product_id),
#         "name": product.get('name', 'Không có tên'),
#         "stock": product.get('stock', 0)
#     }, status=200)
#
# # Cập nhật kho hàng
# @product.put("/api/product/stock/<product_id>/update")
# async def update_stock(request, product_id):
#     try:
#         product_id = ObjectId(product_id)
#     except Exception:
#         raise SanicException("ID sản phẩm không hợp lệ", status_code=400)
#
#     data = request.json
#     quantity = data.get('quantity')
#     if quantity is None or not isinstance(quantity, int):
#         return json({"error": "Số lượng phải là một số nguyên và không được để trống!"}, status=400)
#
#     try:
#         product = db.read_product({"_id": product_id})
#     except Exception as e:
#         return json({"error": f"Lỗi khi truy vấn dữ liệu: {str(e)}"}, status=500)
#
#     if not product:
#         raise SanicException("Sản phẩm không tồn tại", status_code=404)
#
#     try:
#         db.update_product(
#             {"_id": product_id},
#             {"$inc": {"stock": quantity}}
#         )
#     except Exception as e:
#         return json({"error": f"Lỗi khi cập nhật dữ liệu: {str(e)}"}, status=500)
#
#     return json({
#         "message": "Số lượng sản phẩm đã được cập nhật!",
#         "product_id": str(product_id),
#         "updated_stock": product['stock'] + quantity
#     }, status=200)
