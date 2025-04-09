from .admin_routes import router as admin_router

from .user_routes import router as user_router

from .auth import router as auth_router
__all__ = ["admin_router", "user_router", "auth_router"]