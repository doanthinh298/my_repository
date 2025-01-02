# from sanic import Sanic
# from sanic.response import json
# from sanic.request import Request
# from App.database.mongodb.database_store import Database
#
# app = Sanic("ProductSearchApp")
#
#
#
# @app.route("/api/products/search", methods=["GET"])
# async def search_products(request: Request):
#     keyword = request.args.get("keyword", "")
#     category = request.args.get("category", "")
#     min_price = request.args.get("min_price", type=float)
#     max_price = request.args.get("max_price", type=float)
#
#     # Tạo bộ lọc tìm kiếm
#     filter_query = {}
#
#     if keyword:
#         filter_query["name"] = {"$regex": keyword, "$options": "i"}
#     if category:
#         filter_query["category"] = category
#     if min_price is not None:
#         filter_query["price"] = {"$gte": min_price}
#     if max_price is not None:
#         if "price" not in filter_query:
#             filter_query["price"] = {}
#         filter_query["price"]["$lte"] = max_price
#
#     products = products_collection.find(filter_query)
#     product_list = [product for product in products]
#
#     return json({"products": product_list})
#
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8000)
