from datetime import datetime

from pymongo import MongoClient
from bson.objectid import ObjectId

class Database:
    def __init__(self, connection_url=None):

        self.connection_url = connection_url if connection_url else "mongodb://localhost:27017"
        self.client = MongoClient(self.connection_url)
        self.db = self.client['my_data']
        self.Order = self.db["Order"]
        self.Product = self.db["Product"]
        self.User = self.db["User"]
        self.Cart = self.db["Cart"]

        # CRUD cho Order

    def create_order(self, order_data):
        order_data['id'] = str(self.Order.count_documents({}) + 1)
        order_data['status'] = 'pending'
        order_data['created_at'] = order_data.get('created_at', datetime.now())
        return self.Order.insert_one(order_data).inserted_id

    def read_order(self, order_id):
        return self.Order.find_one({"id": order_id})

    def update_order(self, order_id, update_data):
        if 'status' in update_data:
            update_data['updated_at'] = datetime.now()
        return self.Order.update_one({"id": order_id}, {"$set": update_data})

    def delete_order(self, order_id):
        return self.Order.delete_one({"id": order_id})

        # CRUD cho Product

    def create_product(self, product_data):
        return self.Product.insert_one(product_data).inserted_id

    def read_all_products(self):
        return self.Product.find()

    def read_product(self, product_id):
        return self.Product.find_one({"_id": ObjectId(product_id)})

    def update_product(self, product_id, update_data):
        return self.Product.update_one({"_id": ObjectId(product_id)}, {"$set": update_data})

    def delete_product(self, product_id):
        return self.Product.delete_one({"_id": ObjectId(product_id)})
    def find_product_by_name(self, product_name):

        product = self.Product.find_one({"name": product_name})
        if not product:
            return {"error": f"Product with name '{product_name}' not found"}

        count = self.Product.count_documents({"name": product_name})
        if count > 1:
            return {"error": f"Multiple products found with name '{product_name}'. Please refine your search."}
        return product

        # CRUD cho User

    def find_by_user(self, name):
        return self.User.find_one({"name": name})

    def create_user(self, user_data):
        if self.db.User.find_one({"email": user_data["email"]}) or self.db.User.find_one({"name": user_data["name"]}):
            return None
        result = self.db.User.insert_one(user_data)
        return result.inserted_id

    def find_register_user(self, name):
        return self.User.find_one({"name": name})

    def register_user(self, user_data):
        user_data['user_id'] = str(self.User.count_documents({}) + 1)
        self.User.insert_one(user_data)

    def read_user(self, user_id):
        return self.User.find_one({"_id": ObjectId(user_id)})

    def update_user(self, user_id, update_data):
        return self.User.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})

    def delete_user(self, user_id):
        return self.User.delete_one({"_id": ObjectId(user_id)})
        # CRUD cho Cart

    def create_cart(self, cart_data):
        cart_data['id'] = str(self.Cart.count_documents({}) + 1)
        return self.Cart.insert_one(cart_data).inserted_id

    def read_cart(self, user_id):
        return self.Cart.find_one({"user_id": user_id}, {"_id": 0})

    def update_cart(self, cart_id, update_data):
        return self.Cart.update_one({"id": cart_id}, {"$set": update_data}, upsert=True)

    def delete_cart(self, cart_id):
        return self.Cart.delete_one({"id": cart_id})

        # Tìm kiếm theo email hoặc tên

    def find_by_email(self, email):
        return self.User.find_one({"email": email})

    def find_user(self, username):
        return self.User.find_one({"name": username})