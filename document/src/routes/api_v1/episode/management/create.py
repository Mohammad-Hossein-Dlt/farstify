from ._router import router
from fastapi import Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.episode.create_episode_input import CreateEpisodeInput
from src.repo.interface.episode.Iepisode_repo import IEpisodeRepo
from src.routes.depends.repo_depend import episode_repo_depend
from src.repo.interface.Istorage_repo import IStorageRepo
from src.routes.depends.storage_depend import storage_repo_depend
from src.usecases.episode.management.create import CreateEpisode
from src.infra.exceptions.exceptions import AppBaseException

@router.post(
    "/",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def create(
    entity: CreateEpisodeInput = Query(...),
    episode_repo: IEpisodeRepo = Depends(episode_repo_depend),
    storage_repo: IStorageRepo = Depends(storage_repo_depend),
):
    try:
        create_episode_usecase = CreateEpisode(episode_repo, storage_repo)
        output = await create_episode_usecase.execute(entity)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
