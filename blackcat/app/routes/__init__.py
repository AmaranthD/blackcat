from .identities import router as identities_router
from .applications import router as applications_router
from .entitlements import router as entitlements_router
from .assignments import router as assignments_router

__all__ = ["identities_router", "applications_router", "entitlements_router", "assignments_router"]
