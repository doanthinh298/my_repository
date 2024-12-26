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

    def create_order(self, order_data):
        return self.Order.insert_one(order_data).inserted_id

    def read_order(self, order_id):
        return self.Order.find_one({"_id": ObjectId(order_id)})

    def update_order(self, order_id, update_data):
        return self.Order.update_one({"_id": ObjectId(order_id)}, {"$set": update_data})

    def delete_order(self, order_id):
        return self.Order.delete_one({"_id": ObjectId(order_id)})

    def create_product(self, product_data):
        return self.Product.insert_one(product_data).inserted_id

    def create_product_many(self,product_data):
        return self.Product.insert_many(product_data)

    def read_product(self, product_id):
        return self.Product.find_one({"_id": ObjectId(product_id)})

    def update_product(self, product_id, update_data):
        return self.Product.update_one({"_id": ObjectId(product_id)}, {"$set": update_data})

    def delete_product(self, product_id):
        return self.Product.delete_one({"_id": ObjectId(product_id)})

    def find_by_user(self, name):
        return self.User.find_one({"name": name})

    def create_user(self, user_data):
        return self.User.insert_one(user_data).inserted_id

    def find_register_user(self, email):
        return self.User.find_one({"email": email})

    def register_user(self, user_data):
        user_data['user_id'] = str(self.User.count_documents({}) + 1)
        self.User.insert_one(user_data)

    def read_user(self, user_id):
        return self.User.find_one({"_id": ObjectId(user_id)})

    def update_user(self, user_id, update_data):
        return self.User.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})

    def delete_user(self, user_id):
        return self.User.delete_one({"_id": ObjectId(user_id)})


if __name__ == "__main__":
    db = Database()


