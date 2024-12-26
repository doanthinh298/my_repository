from typing import Optional


from pydantic import BaseModel, Field


class Product(BaseModel):
    _id: Optional[int] = None
    name: Optional[str] = None
    price: Optional[int]  = None
    description: Optional[str]  = None


class Order(BaseModel):
    _id: Optional[int] = None
    order_date: Optional[int] = None
    status: Optional[int] = None


class User(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[int] = None


class Create_Product(BaseModel):
    name :str
    category:str
    price: int
    stock : int

class Update_Product(BaseModel):
    name: str
    category: str
    price: int
    stock: int

class Login_User(BaseModel):
    name: str
    email: Optional[str] =None
    password: str
    address: Optional[str] =None
    phone: Optional[int] =None


class Register_User(BaseModel):
    name: str
    email: str
    password: str
    address: str
    phone: int