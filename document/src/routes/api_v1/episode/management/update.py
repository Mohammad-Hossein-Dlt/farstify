from ._router import router
from fastapi import Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.episode.update_episode_input import UpdateEpisodeInput
from src.repo.interface.episode.Iepisode_repo import IEpisodeRepo
from src.routes.depends.repo_depend import episode_repo_depend
from src.repo.interface.Istorage_repo import IStorageRepo
from src.routes.depends.storage_depend import storage_repo_depend
from src.usecases.episode.management.update import UpdateEpisode
from src.infra.exceptions.exceptions import AppBaseException

@router.put(
    "/",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def update(
    entity: UpdateEpisodeInput = Query(...),
    episode_repo: IEpisodeRepo = Depends(episode_repo_depend),
    storage_repo: IStorageRepo = Depends(storage_repo_depend),
):
    try:        
        update_episode_usecase = UpdateEpisode(episode_repo, storage_repo)
        output = await update_episode_usecase.execute(entity)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
