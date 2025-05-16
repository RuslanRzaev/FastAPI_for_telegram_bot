import json
from typing import List
from fastapi import WebSocket, WebSocketDisconnect, Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.utils import post_api
import app.db.requests as rq

kitchen_router = APIRouter(prefix='/kitchen', tags=['kitchen'])
templates = Jinja2Templates(directory="templates")


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@kitchen_router.get("/", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("kitchen.html", {"request": request})


@kitchen_router.websocket("/ws/orders")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@kitchen_router.post("/new_order/")
async def new_order(order: dict):
    order_json = json.dumps(order, ensure_ascii=False)
    await manager.broadcast(order_json)
    return {"message": "Order sent"}


@kitchen_router.get("/get_orders/")
async def get_orders():
    return await rq.get_orders_status('Готовится⌛')


@kitchen_router.get('/ready_order/{order_id}')
async def ready_order(order_id: int):
    await rq.ready_order(order_id)
    return 200


@kitchen_router.get('/close_order/{order_id}')
async def close_order(order_id: int):
    await rq.close_order(order_id)
    return 200


@kitchen_router.post("/verify_code/{order_id}")
async def verify_code(order_id: int, data: dict):
    code = data.get("code")
    if int(code) == order_id:
        await rq.ready_order(order_id)
        await post_api('cashier/new_order/',
                       json={"id": order_id, "items": await rq.items_in_order(order_id)})
        return {"success": True}
    return {"success": False}
