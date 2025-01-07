import copy
from datetime import datetime


class Order:
    def __init__(self, _id='', user_id='', products=None, total_price=0, shipping_address='', status='pending',
                 created_at=None, updated_at=None):
        self._id = _id
        self.user_id = user_id
        self.products = products or []
        self.total_price = total_price
        self.shipping_address = shipping_address
        self.status = status
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def to_dict(self):
        order_dict = copy.deepcopy(self.__dict__)
        order_dict['created_at'] = self.created_at.isoformat()
        order_dict['updated_at'] = self.updated_at.isoformat()
        return order_dict

    @classmethod
    def from_dict(cls, json_dict: dict):
        created_at = json_dict.get('created_at')
        updated_at = json_dict.get('updated_at')

        if created_at:
            created_at = datetime.fromisoformat(created_at)
        if updated_at:
            updated_at = datetime.fromisoformat(updated_at)

        return cls(
            _id=json_dict.get('_id', ''),
            user_id=json_dict.get('user_id', ''),
            products=json_dict.get('products', []),
            total_price=json_dict.get('total_price', 0),
            shipping_address=json_dict.get('shipping_address', ''),
            status=json_dict.get('status', 'pending'),
            created_at=created_at,
            updated_at=updated_at
        )

    def __eq__(self, other):
        # So sánh đối tượng
        return self._id == other._id

    def __hash__(self):
        # Hàm băm cho đối tượng
        return hash(self._id)
