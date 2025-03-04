from fastapi import FastAPI
from app.routers.admin_routes import router as admin_router
from app.routers.user_routes import router as user_router
from app.routers.super_admin_routes import router as super_admin_routes
app = FastAPI()

app.include_router(admin_router)
app.include_router(user_router)
app.include_router(super_admin_routes)

