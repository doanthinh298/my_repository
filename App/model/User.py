import copy

class User:
    def __init__(self,name,email,password,address,phone,id ):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.address = address
        self.phone = phone

    def to_dict(self):
        return {
            "id": self.id,
            "name":self.name,
            "email":self.email,
            "password": self.password,
            "address": self.address,
            "phone":self.phone
        }

    @classmethod
    def from_dict(cls, json_dict: dict):
        id = json_dict['_id']
        user = User(id)
        user.name = json_dict['name']
        user.email = json_dict['email']
        user.password = json_dict['password']
        user.address = json_dict["address"]
        user.phone = json_dict["phone"]

    def to_dict(self):
        return copy.deepcopy(self.__dict__)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

