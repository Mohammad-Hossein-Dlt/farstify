from fastapi import APIRouter

from src.routes.api_v1.user._router import router as user_router
from src.routes.api_v1.image._router import router as image_router
from src.routes.api_v1.link._router import router as link_router
from src.routes.api_v1.follow._router import router as follow_router
from src.routes.api_v1.like._router import router as like_router
from src.routes.api_v1.playlist.management._router import router as playlist_router
from src.routes.api_v1.playlist.item._router import router as playlist_item_router

from src.routes.api_v1.metrics._router import router as metrics_router
from src.routes.api_v1.health_check._router import router as health_check_router

ROUTE_PREFIX_VERSION_API = "/api/v1"

main_router_v1 = APIRouter()

main_router_v1.include_router(user_router, prefix=ROUTE_PREFIX_VERSION_API)
main_router_v1.include_router(image_router, prefix=ROUTE_PREFIX_VERSION_API)
main_router_v1.include_router(link_router, prefix=ROUTE_PREFIX_VERSION_API)
main_router_v1.include_router(follow_router, prefix=ROUTE_PREFIX_VERSION_API)
main_router_v1.include_router(like_router, prefix=ROUTE_PREFIX_VERSION_API)
main_router_v1.include_router(playlist_router, prefix=ROUTE_PREFIX_VERSION_API)
main_router_v1.include_router(playlist_item_router, prefix=ROUTE_PREFIX_VERSION_API)

main_router_v1.include_router(metrics_router, prefix=ROUTE_PREFIX_VERSION_API)
main_router_v1.include_router(health_check_router, prefix=ROUTE_PREFIX_VERSION_API)
