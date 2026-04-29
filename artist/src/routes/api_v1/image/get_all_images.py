from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.filter.sort_direction_filter_input import SortDirectionFilterInput
from src.repo.interface.Iartist_repo import IArtistRepo
from src.routes.depends.repo_depend import artist_repo_depend
from src.repo.interface.Iartist_image_repo import IArtistImageRepo
from src.routes.depends.repo_depend import artist_image_repo_depend
from src.repo.interface.Istorage_repo import IStorageRepo
from src.routes.depends.storage_depend import storage_repo_depend
from src.usecases.image.get_all_images import GetAllImages
from src.infra.exceptions.exceptions import AppBaseException

@router.get(
    "/all",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def get_all_images(
    to_filter: SortDirectionFilterInput = Query(...),
    artist_repo: IArtistRepo = Depends(artist_repo_depend),
    artist_image_repo: IArtistImageRepo = Depends(artist_image_repo_depend),
    storage_repo: IStorageRepo = Depends(storage_repo_depend),
):
    try:
        get_all_images_usecase = GetAllImages(artist_repo, artist_image_repo, storage_repo)
        outputs_list = await get_all_images_usecase.execute(to_filter)
        return [ output.model_dump(mode="json") for output in outputs_list ]
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
