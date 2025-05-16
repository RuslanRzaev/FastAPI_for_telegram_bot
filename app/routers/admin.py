import json
from app.utils import result_to_json
from fastapi import APIRouter
from app.schemas import CategoryBase, ItemsBase, CategoryUpdate, ItemsUpdate
from app.db import requests as rq

admin_router = APIRouter(prefix='/admin', tags=['admin'])


@admin_router.get('/get_users')
async def get_users():
    return await rq.get_users()

@admin_router.post('/category', response_model=CategoryBase)
async def category(category: CategoryBase):
    category = json.loads(category.model_dump_json())
    await rq.add_category(category)
    return category


@admin_router.patch('/category/{category_id}', response_model=CategoryUpdate)
async def edit_category(category_id: int, category_data: CategoryUpdate):
    category_data = json.loads(category_data.model_dump_json())
    print(category_data['name'])
    await rq.edit_category(category_id, category_data['name'])
    return category_data

@admin_router.delete('/category/{category_id}')
async def delete_category(category_id: int):
    await rq.delete_category(category_id)
    return 200

@admin_router.patch('/items/{items_id}', response_model=ItemsUpdate)
async def edit_items(items_id: int, items_data: ItemsUpdate):
    items_data = json.loads(items_data.model_dump_json())
    print(items_data)
    for key in items_data:
        if items_data[key] != None:
            await rq.edit_items(items_id, key, items_data[key])
    return items_data

@admin_router.delete('/items/{items_id}')
async def delete_items(items_id: int):
    await rq.delete_items(items_id)
    return 200



@admin_router.post('/items', response_model=ItemsBase)
async def items(item: ItemsBase):
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

@admin_router.get('/all_orders')
async def all_orders():
    return result_to_json(await rq.all_orders_rq())