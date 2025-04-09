from fastapi import FastAPI
from app.routers.admin_routes import router as admin_router
from app.routers.user_routes import router as user_router
from app.routers.super_admin_routes import router as super_admin_routes
from app.routers.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

app.include_router(admin_router)
app.include_router(user_router)
app.include_router(super_admin_routes)
app.include_router(auth_router)

