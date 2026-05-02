from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from document.src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria
from src.repo.interface.episode.Iepisode_repo import IEpisodeRepo
from src.routes.depends.repo_depend import episode_repo_depend
from src.usecases.episode.management.get_by_document_id import GetAllEpisodes
from src.infra.exceptions.exceptions import AppBaseException

@router.get(
    "/all",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def get_by_document_id(
    document_id: str = Query(...),
    criteria: BaseFilterCriteria = Depends(),
    episode_repo: IEpisodeRepo = Depends(episode_repo_depend),
):
    try:
        get_all_episodes_usecase = GetAllEpisodes(episode_repo)
        outputs_list = await get_all_episodes_usecase.execute(document_id, criteria)
        return [ output.model_dump(mode="json") for output in outputs_list ]
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
