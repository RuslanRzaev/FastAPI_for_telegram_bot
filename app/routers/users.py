from fastapi import APIRouter
from app.db import requests as rq
from app.to_json import result_to_json
user_router = APIRouter(prefix='/user', tags=['user'])


@user_router.post("/login/{telegram_id}")
async def login(telegram_id: int):
    await rq.login_user(telegram_id)
    return {"authorization": 'ok'}


@user_router.get('/get_categories')
async def get_categories():
    return await rq.get_categories()


@user_router.get('/get_items/<categories_id>')
async def get_items(categories_id: int):
    return rq.get_items(categories_id)
