import copy
from datetime import datetime

class Cart:
    def __init__(self, _id='', id='', user_id='', name='', products=None, total_price=0, created_at=None, updated_at=None):
        self._id = _id
        self.id = id
        self.user_id = user_id
        self.name = name
        self.products = products if products is not None else []
        self.total_price = total_price
        self.created_at = created_at if created_at else datetime.utcnow()
        self.updated_at = updated_at if updated_at else datetime.utcnow()

    def to_dict(self):
        return copy.deepcopy(self.__dict__)

    @classmethod
    def from_dict(cls, json_dict: dict):
        _id = json_dict.get('_id', '')
        id = json_dict.get('id', '')
        user_id = json_dict['user_id']
        name = json_dict['name']
        products = json_dict['products']
        total_price = json_dict['total_price']
        created_at = datetime.fromisoformat(json_dict['created_at'])
        updated_at = datetime.fromisoformat(json_dict['updated_at'])

        cart = cls(_id, id, user_id, name, products, total_price, created_at, updated_at)
        return cart

    def update(self, products, name, total_price):
        self.name = name
        self.products = products
        self.total_price = total_price
        self.updated_at = datetime.utcnow()

    def __eq__(self, other):
        return self._id == other._id

    def __hash__(self):
        return hash(self._id)
