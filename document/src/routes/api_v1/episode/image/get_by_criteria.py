from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.filter.sort_direction_filter_input import SortDirectionFilterInput
from src.repo.interface.episode.Iepisode_repo import IEpisodeRepo
from src.routes.depends.repo_depend import episode_repo_depend
from src.repo.interface.episode.Iepisode_image_repo import IEpisodeImageRepo
from src.routes.depends.repo_depend import episode_image_repo_depend
from src.repo.interface.Istorage_repo import IStorageRepo
from src.routes.depends.storage_depend import storage_repo_depend
from src.usecases.episode.image.get_by_criteria import GetAllImages
from src.infra.exceptions.exceptions import AppBaseException

@router.get(
    "/all",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def get_by_criteria(
    criteria: SortDirectionFilterInput = Query(...),
    episode_repo: IEpisodeRepo = Depends(episode_repo_depend),
    episode_image_repo: IEpisodeImageRepo = Depends(episode_image_repo_depend),
    storage_repo: IStorageRepo = Depends(storage_repo_depend),
):
    try:
        get_all_images_usecase = GetAllImages(episode_repo, episode_image_repo, storage_repo)
        outputs_list = await get_all_images_usecase.execute(criteria)
        return [ output.model_dump(mode="json") for output in outputs_list ]
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
