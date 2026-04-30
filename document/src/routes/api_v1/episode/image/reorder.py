from ._router import router
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.repo.interface.episode.Iepisode_repo import IEpisodeRepo
from src.routes.depends.repo_depend import episode_repo_depend
from src.repo.interface.episode.Iepisode_image_repo import IEpisodeImageRepo
from src.routes.depends.repo_depend import episode_image_repo_depend
from src.usecases.episode.image.reorder import ReorderImages
from src.infra.exceptions.exceptions import AppBaseException

@router.put(
    "/reorder",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def reorder(
    episode_id: str,
    image_ids: list[str],
    episode_repo: IEpisodeRepo = Depends(episode_repo_depend),
    episode_image_repo: IEpisodeImageRepo = Depends(episode_image_repo_depend),
):
    try:
        reorder_images_usecase = ReorderImages(episode_repo, episode_image_repo)
        outputs_list = await reorder_images_usecase.execute(episode_id, image_ids)
        return [ output.model_dump(mode="json") for output in outputs_list ]
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
