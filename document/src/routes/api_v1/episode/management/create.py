from ._router import router
from fastapi import UploadFile, Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.episode.create_episode_input import CreateEpisodeInput
from src.repo.interface.document.Idocument_repo import IDocumentRepo
from src.routes.depends.repo_depend import document_repo_depend
from src.repo.interface.episode.Iepisode_repo import IEpisodeRepo
from src.routes.depends.repo_depend import episode_repo_depend
from src.repo.interface.Icache import ICacheRepo
from src.routes.depends.cache_depend import cache_repo_depend
from src.repo.interface.Istorage_repo import IStorageRepo
from src.routes.depends.storage_depend import storage_repo_depend
from src.gateway.interface.Ibroker_service import IBrokerService
from src.routes.depends.services_depend import convert_service_depend
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
    file: UploadFile | None = None,
    entity: CreateEpisodeInput = Query(...),
    document_repo: IDocumentRepo = Depends(document_repo_depend),
    episode_repo: IEpisodeRepo = Depends(episode_repo_depend),
    cache_repo: ICacheRepo = Depends(cache_repo_depend),
    storage_repo: IStorageRepo = Depends(storage_repo_depend),
    broker_service: IBrokerService = Depends(convert_service_depend),
):
    try:
        create_episode_usecase = CreateEpisode(document_repo, episode_repo, cache_repo, storage_repo, broker_service)
        if file:
            output = await create_episode_usecase.execute(
                entity,
                file.file,
                file.filename,
                file.size,
                file.content_type,
            )
        else:
            output = await create_episode_usecase.execute(entity)
            
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
