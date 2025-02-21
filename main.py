from fastapi import FastAPI

from routers import admin_router , user_router

app = FastAPI()

app.include_router(admin_router)
app.include_router(user_router)