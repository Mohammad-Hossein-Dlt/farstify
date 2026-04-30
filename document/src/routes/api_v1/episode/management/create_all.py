from ._router import router
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.repo.interface.episode.Iepisode_repo import IEpisodeRepo
from src.routes.depends.repo_depend import episode_repo_depend
from src.usecases.episode.management.create_all import CreateAllEpisodes
from data.episodes import all_episode
from src.infra.exceptions.exceptions import AppBaseException

@router.post(
    "/all",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def create_all(
    episode_repo: IEpisodeRepo = Depends(episode_repo_depend),
):
    try:
        create_episodes_usecase = CreateAllEpisodes(episode_repo)
        output = await create_episodes_usecase.execute(all_episode)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
