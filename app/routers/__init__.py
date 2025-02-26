from .admin_routes import router as admin_router

from .user_routes import router as user_router

__all__ = ["admin_router", "user_router"]