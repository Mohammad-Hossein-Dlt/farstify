from ._router import router
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.repo.interface.episode.Iepisode_repo import IEpisodeRepo
from src.routes.depends.repo_depend import episode_repo_depend
from src.repo.interface.episode.Iepisode_image_repo import IEpisodeImageRepo
from src.routes.depends.repo_depend import episode_image_repo_depend
from src.repo.interface.episode.Iepisode_link_repo import IEpisodeLinkRepo
from src.routes.depends.repo_depend import episode_link_repo_depend
from src.repo.interface.Istorage_repo import IStorageRepo
from src.routes.depends.storage_depend import storage_repo_depend
from src.usecases.episode.management.delete_by_document_id import DeleteAllEpisodes
from src.infra.exceptions.exceptions import AppBaseException

@router.delete(
    "/all",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def delete_by_document_id(
    document_id: str,
    episode_repo: IEpisodeRepo = Depends(episode_repo_depend),
    episode_image_repo: IEpisodeImageRepo = Depends(episode_image_repo_depend),
    episode_link_repo: IEpisodeLinkRepo = Depends(episode_link_repo_depend),
    storage_repo: IStorageRepo = Depends(storage_repo_depend),
):
    try:
        delete_all_episodes_usecase = DeleteAllEpisodes(episode_repo, episode_image_repo, episode_link_repo, storage_repo)
        output = await delete_all_episodes_usecase.execute(document_id)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
