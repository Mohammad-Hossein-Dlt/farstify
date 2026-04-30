from ._router import router
from fastapi import Depends
from src.routes.depends.db_health_check_depend import db_health_check_depend

@router.get("")
async def health_check(
    db_status: bool = Depends(db_health_check_depend),
):
    status = "Ok" if db_status else "Inaccessible!"
    return {
        "status": status,
    }
