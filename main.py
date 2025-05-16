from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from app.routers import user_router, admin_router, cashier_router, kitchen_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user_router)
app.include_router(admin_router)
app.include_router(kitchen_router)
app.include_router(cashier_router)
