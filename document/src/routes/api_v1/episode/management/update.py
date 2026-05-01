from ._router import router
from fastapi import UploadFile, Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.episode.update_episode_input import UpdateEpisodeInput
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
    file: UploadFile | None = None,
    entity: UpdateEpisodeInput = Query(...),
    document_repo: IDocumentRepo = Depends(document_repo_depend),
    episode_repo: IEpisodeRepo = Depends(episode_repo_depend),
    cache_repo: ICacheRepo = Depends(cache_repo_depend),
    storage_repo: IStorageRepo = Depends(storage_repo_depend),
    broker_service: IBrokerService = Depends(convert_service_depend),
):
    try:        
        update_episode_usecase = UpdateEpisode(document_repo, episode_repo, cache_repo, storage_repo, broker_service)
        if file:
            output = await update_episode_usecase.execute(
                entity,
                file.file,
                file.filename,
                file.size,
                file.content_type,
            )
        else:
            output = await update_episode_usecase.execute(entity)
            
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
