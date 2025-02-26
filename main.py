from fastapi import FastAPI
from app.routers.admin_routes import router as admin_router
from app.routers.user_routes import router as user_router

app = FastAPI()

app.include_router(admin_router)
app.include_router(user_router)
