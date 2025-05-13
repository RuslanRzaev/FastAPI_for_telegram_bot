import json

from fastapi import APIRouter
from app.schemas import CategoryBase, ItemsBase
from app.db import requests as rq

admin_router = APIRouter(prefix='/admin', tags=['admin'])


@admin_router.post('/category', response_model=CategoryBase)
async def category(category: CategoryBase):
    category = json.loads(category.model_dump_json())
    await rq.add_category(category)
    return category


@admin_router.post('/items', response_model=ItemsBase)
async def add_items(item: ItemsBase):
    item = json.loads(item.model_dump_json())
    await rq.add_items(item)
    return item


@admin_router.get('/count_orders_day')
async def count_orders_day():
    return await rq.count_orders_day()


@admin_router.get('/count_orders_month')
async def count_orders_month():
    return await rq.count_orders_month()


@admin_router.get('/turnover_orders_day')
async def turnover_orders_day():
    return await rq.turnover_orders_day()


@admin_router.get('/turnover_orders_month')
async def turnover_orders_month():
    return await rq.turnover_orders_month()


@admin_router.get('/revenue_orders_day')
async def revenue_orders_day():
    return await rq.revenue_orders_day()


@admin_router.get('/revenue_orders_month')
async def revenue_orders_month():
    return await rq.revenue_orders_month()


@admin_router.get('/average_bill_today')
async def average_bill_today():
    return (await rq.turnover_orders_day() / await rq.count_orders_day()) if await rq.count_orders_day() else 0


@admin_router.get('/average_bill_month')
async def average_bill_month():
    return (await rq.turnover_orders_month() / await rq.count_orders_month()) if await rq.count_orders_month() else 0


