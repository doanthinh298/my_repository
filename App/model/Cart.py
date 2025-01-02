import copy
from datetime import datetime

class Cart:
    def __init__(self, _id='', user_id='', products=None, total_price=0, created_at=None, updated_at=None):
        self._id = _id
        self.user_id = user_id
        self.products = products if products is not None else []
        self.total_price = total_price
        self.created_at = created_at if created_at else datetime.utcnow()
        self.updated_at = updated_at if updated_at else datetime.utcnow()
    def to_dict(self):
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "products": self.products,
            "total_price": self.total_price,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    @classmethod
    def from_dict(cls, json_dict: dict):
        _id = json_dict['_id']
        user_id = json_dict['user_id']
        products = json_dict['products']
        total_price = json_dict['total_price']
        created_at = datetime.fromisoformat(json_dict['created_at'])
        updated_at = datetime.fromisoformat(json_dict['updated_at'])

        cart = cls(_id, user_id, products, total_price, created_at, updated_at)
        return cart

    def update(self, products, total_price):
        self.products = products
        self.total_price = total_price
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return copy.deepcopy(self.__dict__)

    def __eq__(self, other):
        return self._id == other._id

    def __hash__(self):
        return hash(self._id)

