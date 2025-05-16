import json
import qrcode

from fastapi import APIRouter
from io import BytesIO

from starlette.responses import StreamingResponse

from app.schemas import UserBase, OrderBase

from app.db import requests as rq
from app.utils import result_to_json, ADMINS, KITCHEN

user_router = APIRouter(prefix='/user', tags=['user'])


@user_router.post("/login", response_model=UserBase)
async def login(User: UserBase):
    user = json.loads(User.model_dump_json())
    await rq.login_user(user['telegram_id'], user['first_name'])
    return UserBase(**user)


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


@user_router.get('/add_bucket/{telegram_id}/{item_id}')
async def add_bucket(telegram_id: int, item_id: int):
    await rq.add_busket(telegram_id, item_id)
    return 200


@user_router.get('/delete_bucket/{telegram_id}/{item_id}')
async def delete_bucket(telegram_id: int, item_id: int):
    await rq.delete_busket(telegram_id, item_id)
    return 200


@user_router.get('/is_item_in_basket/{telegram_id}/{item_id}')
async def is_item_in_basket(telegram_id: int, item_id: int):
    return await rq.is_item_in_basket(telegram_id, item_id)


@user_router.get('/bucket/{telegram_id}')
async def bucket(telegram_id: int):
    return result_to_json(await rq.get_my_basket(telegram_id))

@user_router.post('/order', response_model=OrderBase)
async def add_order(Order: OrderBase):
    order = json.loads(Order.model_dump_json())
    await rq.add_order(order['telegram_id'], order['items'], order['total_price'], order['total_revenue'])
    return OrderBase(**order)

@user_router.get('/order/{telegram_id}')
async def get_order(telegram_id: int):
    return await rq.get_my_order(telegram_id)


@user_router.delete('/order/{telegram_id}')
async def get_order(telegram_id: int):
    await rq.clear_basket(telegram_id)
    return 200

@user_router.get('/items_in_order/{order_id}')
async def items_in_order(order_id: int):
    return await rq.items_in_order(order_id)

@user_router.get('/status_order/{order_id}')
async def status_order(order_id: int):
    return await rq.status_order(order_id)

@user_router.get('/secret_code/{order_id}')
async def secret_code(order_id: int):
    return await rq.secret_code(order_id)

@user_router.get('/price_order/{order_id}')
async def price_order(order_id: int):
    return await rq.price_order(order_id)

@user_router.get('/day_order/{order_id}')
async def day_order(order_id: int):
    return await rq.day_order(order_id)

@user_router.get('/month_order/{order_id}')
async def month_order(order_id: int):
    return await rq.month_order(order_id)

@user_router.get('/year_order/{order_id}')
async def month_order(order_id: int):
    return await rq.year_order(order_id)

@user_router.get('/orders/{telegram_id}')
async def get_orders_user(telegram_id: int):
    return result_to_json(await rq.orders_user(telegram_id))

@user_router.get('/items_in_order/{order_id}')
async def items_in_order(order_id: int):
    return await rq.items_in_order(order_id)

@user_router.get('/user_id_order/{order_id}')
async def user_id_order(order_id: int):
    return await rq.user_id_order(order_id)

@user_router.get('/id_user_order/{order_id}')
async def id_user_order(order_id: int):
    return await rq.id_user_order(order_id)

@user_router.get('/items_id/{item_id}')
async def items_id(item_id):
    return await rq.get_items_id([*item_id])

@user_router.get('/ready_order_bool/{order_id}')
async def ready_order_bool(order_id: int) -> bool:
    return await rq.ready_order_bool(order_id)

@user_router.get('/issued_order_bool/{order_id}')
async def issued_order_bool(order_id: int) -> bool:
    return await rq.issued_order_bool(order_id)

@user_router.get('/finished_orders')
async def finished_orders():
    return await rq.finished_orders()

@user_router.get('/change_send_to_true/{order_id}')
async def change_send_to_true(order_id: int):
    await rq.change_send_to_true(order_id)
    return 200

@user_router.get('/order_qr_code/{order_id}')
async def order_qr_code(order_id: int):
    secret_code = await rq.secret_code(order_id)
    img = qrcode.make(secret_code)
    byte_arr = BytesIO()
    img.save(byte_arr, format='PNG')
    byte_arr.seek(0)
    return StreamingResponse(
        content=byte_arr,
        media_type="image/png",
        headers={"Content-Disposition": f"inline; filename=order_{order_id}_qr.png"}
    )

@user_router.get('/check_admin/{user_id}')
async def check_admin(user_id: int):
    return user_id in ADMINS

@user_router.get('/check_kitchen/{user_id}')
async def check_kitchen(user_id: int):
    return user_id in KITCHEN