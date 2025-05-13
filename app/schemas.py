from pydantic import BaseModel


class UserBase(BaseModel):
    telegram_id: str


class CategoryBase(BaseModel):
    name: str


class ItemsBase(BaseModel):
    name: str
    description: str = None
    cost_price: float | int
    price: float | int
    category_id: int
    img: str = None
