import json

from fastapi import APIRouter
from watchfiles import awatch

from app.db import requests as rq
from app.to_json import result_to_json

user_router = APIRouter(prefix='/user', tags=['user'])


@user_router.post("/login/{telegram_id}")
async def login(telegram_id: int):
    await rq.login_user(telegram_id)
    return {"authorization": 'ok'}


@user_router.get('/category')
async def category():
    return result_to_json(await rq.get_categories())


@user_router.get('/items/{categories_id}')
async def items(categories_id: int):
    return result_to_json(await rq.get_items(categories_id))

@user_router.get('/name_category/{category_id}')
async def name_category(category_id: int):
    return await rq.get_name_category(category_id)

@user_router.get('/item/{item_id}')
async def item(item_id: int):
    return await rq.get_item(item_id)

@user_router.get('/category_id_by_product/{item_id}')
async def category_id_by_product(item_id: int):
    return await rq.get_category_id_by_product(item_id)