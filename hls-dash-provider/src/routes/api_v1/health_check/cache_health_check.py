from ._router import router
from fastapi import Depends
from src.routes.depends.cache_health_check_depend import cache_health_check_depend

@router.get(
    "/cache",
)
async def cache_health_check(
    cache_status: bool = Depends(cache_health_check_depend),
):
    status = "Ok" if cache_status else "Inaccessible!"
    return {
        "status": status,
    }
