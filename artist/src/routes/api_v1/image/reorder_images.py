from ._router import router
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.repo.interface.Iartist_repo import IArtistRepo
from src.routes.depends.repo_depend import artist_repo_depend
from src.repo.interface.Iartist_image_repo import IArtistImageRepo
from src.routes.depends.repo_depend import artist_image_repo_depend
from src.usecases.image.reorder_images import ReorderImages
from src.infra.exceptions.exceptions import AppBaseException

@router.put(
    "/reorder",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def reorder_images(
    artist_id: str,
    image_ids: list[str],
    artist_repo: IArtistRepo = Depends(artist_repo_depend),
    artist_image_repo: IArtistImageRepo = Depends(artist_image_repo_depend),
):
    try:
        reorder_images_usecase = ReorderImages(artist_repo, artist_image_repo)
        outputs_list = await reorder_images_usecase.execute(artist_id, image_ids)
        return [ output.model_dump(mode="json") for output in outputs_list ]
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
