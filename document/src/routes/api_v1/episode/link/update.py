from ._router import router
from fastapi import Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.episode.update_link_input import UpdateLinkInput
from src.repo.interface.episode.Iepisode_link_repo import IEpisodeLinkRepo
from src.routes.depends.repo_depend import episode_link_repo_depend
from src.usecases.episode.link.update import UpdateLink
from src.infra.exceptions.exceptions import AppBaseException

@router.put(
    "/",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def update(
    entity: UpdateLinkInput = Query(...),
    episode_link_repo: IEpisodeLinkRepo = Depends(episode_link_repo_depend),
):
    try:
        update_link_usecase = UpdateLink(episode_link_repo)
        output = await update_link_usecase.execute(entity)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
