import copy

class Product:
    def __init__(self, _id=''):
        self.id = _id
        self.name = ''
        self.description = ''
        self.category = ''
        self.price = ''
        self.stock = ''

    def to_dict(self):
        return copy.deepcopy(self.__dict__)

    @classmethod
    def from_dict(cls, json_dict: dict):
        id_ = json_dict['_id']
        product = Product(id_)
        product.name = json_dict['name']
        product.description = json_dict['description']
        product.category = json_dict['category']
        product.price = json_dict['price']
        product.stock = json_dict['stock']
        return product

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
