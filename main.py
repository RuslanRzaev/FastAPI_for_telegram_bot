from fastapi import FastAPI
from app.routers import user_router, admin_router, kitchen_router
app = FastAPI()

app.include_router(user_router)
app.include_router(admin_router)
app.include_router(kitchen_router)