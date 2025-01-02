import copy

class Order:
    def __init__(self, _id='', user_id='', address='', phone='', items=None, total_price=0, status='pending', created_at=None, updated_at=None):
        self._id = _id
        self.user_id = user_id
        self.address = address
        self.phone = phone
        self.items = items or []
        self.total_price = total_price
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return copy.deepcopy(self.__dict__)

    @classmethod
    def from_dict(cls, json_dict: dict):
        return cls(
            _id=json_dict.get('_id', ''),
            user_id=json_dict.get('user_id', ''),
            address=json_dict.get('address', ''),
            phone=json_dict.get('phone', ''),
            items=json_dict.get('items', []),
            total_price=json_dict.get('total_price', 0),
            status=json_dict.get('status', 'pending'),
            created_at=json_dict.get('created_at', None),
            updated_at=json_dict.get('updated_at', None)
        )

    def __eq__(self, other):
        return self._id == other._id

    def __hash__(self):
        return hash(self._id)
