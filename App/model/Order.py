import copy

class Order:
    def __init__(self, _id = ''):
        self.id =''
        self.order_date = ''
        self.status = ''

    def to_dict(self):
        return {
            "id": self.id,
            "order_date": self.order_date,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, json_dict: dict):
        id_ = json_dict['_id']
        order = Order(id_)
        order.order_date = json_dict['order_date']
        order.status = json_dict['status']

        return order

    def to_dict(self):
        return copy.deepcopy(self.__dict__)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


