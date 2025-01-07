from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class Product(BaseModel):
    _id: Optional[int] = None
    name: Optional[str] = None
    category:str
    price: Optional[int]  = None
    description: Optional[str]  = None


class Create_Product(BaseModel):
    name: str
    description: str
    category: str
    price: int
    stock: int


class Update_Product(BaseModel):
    name: str
    description : str
    category: str
    price: int
    stock: int

class Order(BaseModel):
    user_id: str
    products: List[dict]
    total_price: float
    shipping_address: str
    status: str = 'pending'
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

class User(BaseModel):
    user_id: str
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[int] = None


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

class AddToCartModel(BaseModel):
    name: str
    quantity: int



class GetCart(BaseModel):
    user_id: str
    items: List[AddToCartModel]
    total_price: float
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class UpdateCartModel(BaseModel):
    id: Optional[str] = None
    user_id: str
    product: str
