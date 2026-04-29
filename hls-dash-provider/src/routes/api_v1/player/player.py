from ._router import router
from fastapi import Request, Depends, HTTPException
from src.domain.enums import Format
from src.repo.interface.Istorage_repo import IStorageRepo
from src.routes.depends.storage_depend import storage_repo_depend
from src.usecases.player.player import Player
from src.infra.fastapi_config.template_engine import templates
from src.infra.exceptions.exceptions import AppBaseException

@router.get(
    "/{object_name:path}",
)
async def health_check(
    request: Request,
    format: Format,
    object_name: str,
    storage_repo: IStorageRepo = Depends(storage_repo_depend),
):
    try:
        player_usecase = Player(storage_repo)
        output = player_usecase.execute(object_name, format)
        if format == "dash":
            return templates.TemplateResponse(request, "dash_player.html", {"url": output})
        elif format == "hls":
            return templates.TemplateResponse(request, "hls_player.html", {"url": output})
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))