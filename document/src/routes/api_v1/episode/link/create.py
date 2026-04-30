from ._router import router
from fastapi import Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.episode.create_link_input import CreateLinkInput
from src.repo.interface.episode.Iepisode_repo import IEpisodeRepo
from src.routes.depends.repo_depend import episode_repo_depend
from src.repo.interface.episode.Iepisode_link_repo import IEpisodeLinkRepo
from src.routes.depends.repo_depend import episode_link_repo_depend
from src.usecases.episode.link.create import CreateLink
from src.infra.exceptions.exceptions import AppBaseException

@router.post(
    "/",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def create(
    entity: CreateLinkInput = Query(...),
    episode_repo: IEpisodeRepo = Depends(episode_repo_depend),
    episode_link_repo: IEpisodeLinkRepo = Depends(episode_link_repo_depend),
):
    try:
        create_link_usecase = CreateLink(episode_repo, episode_link_repo)
        output = await create_link_usecase.execute(entity)            
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
