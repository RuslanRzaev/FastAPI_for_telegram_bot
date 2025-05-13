from app.db.database import engine
from dotenv import load_dotenv
from sqlalchemy import BigInteger, Float, ForeignKey, Integer, Text, String
from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

load_dotenv()


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)

    tg_id: Mapped[int] = mapped_column(BigInteger)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    orders: Mapped[list['Order']] = relationship(back_populates='user')


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(Text)


class Item(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    cost_price: Mapped[float] = mapped_column(Float)
    price: Mapped[float] = mapped_column(Float)
    category: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    img: Mapped[str] = mapped_column(Text)


class Basket(Base):
    __tablename__ = 'basket'
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    user: Mapped[int] = mapped_column(ForeignKey('users.id'))
    item: Mapped[int] = mapped_column(ForeignKey('items.id'))
    count: Mapped[int] = mapped_column(Integer)


class Order(Base):
    __tablename__ = 'Order'
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    items: Mapped[str] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Float)
    revenue: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(Text)
    log_status: Mapped[str] = mapped_column(Text)
    secret_code: Mapped[str] = mapped_column(Text)
    year: Mapped[int] = mapped_column(Integer)
    month: Mapped[int] = mapped_column(Integer)
    day: Mapped[int] = mapped_column(Integer)

    user = relationship('User', back_populates='orders')


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
