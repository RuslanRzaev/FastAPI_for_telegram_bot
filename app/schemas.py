from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    telegram_id: str
    first_name: str


class CategoryBase(BaseModel):
    name: str

class CategoryUpdate(BaseModel):
    name: Optional[str] = None


class ItemsBase(BaseModel):
    name: str
    description: str
    cost_price: float | int
    price: float | int
    category_id: int
    img: str

class ItemsUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    cost_price: Optional[float | int] = None
    price: Optional[float | int]  = None
    category_id: Optional[int]  = None
    img: Optional[str]  = None

class OrderBase(BaseModel):
    telegram_id: Optional[int] = None
    items: Optional[str] = None
    total_price: Optional[float | int] = None
    total_revenue: Optional[float | int] = None