from fastapi import APIRouter

from src.routes.api_v1.document.management._router import router as document_management_router
from src.routes.api_v1.document.image._router import router as document_image_router
from src.routes.api_v1.document.link._router import router as document_link_router

from src.routes.api_v1.episode.management._router import router as episode_management_router
from src.routes.api_v1.episode.image._router import router as episode_image_router
from src.routes.api_v1.episode.link._router import router as episode_link_router

from src.routes.api_v1.metrics._router import router as metrics_router
from src.routes.api_v1.health_check._router import router as health_check_router

ROUTE_PREFIX_VERSION_API = "/api/v1"

main_router_v1 = APIRouter()

main_router_v1.include_router(document_management_router, prefix=ROUTE_PREFIX_VERSION_API)
main_router_v1.include_router(document_image_router, prefix=ROUTE_PREFIX_VERSION_API)
main_router_v1.include_router(document_link_router, prefix=ROUTE_PREFIX_VERSION_API)

main_router_v1.include_router(episode_management_router, prefix=ROUTE_PREFIX_VERSION_API)
main_router_v1.include_router(episode_image_router, prefix=ROUTE_PREFIX_VERSION_API)
main_router_v1.include_router(episode_link_router, prefix=ROUTE_PREFIX_VERSION_API)

main_router_v1.include_router(metrics_router, prefix=ROUTE_PREFIX_VERSION_API)
main_router_v1.include_router(health_check_router, prefix=ROUTE_PREFIX_VERSION_API)