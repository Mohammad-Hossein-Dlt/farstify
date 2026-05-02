from ._router import router
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.repo.interface.Iuser_link_repo import IUserLinkRepo
from src.routes.depends.repo_depend import user_link_repo_depend
from src.usecases.link.reorder import ReorderLinks
from src.infra.exceptions.exceptions import AppBaseException

@router.put(
    "/reorder",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def reorder(
    user_id: str,
    link_ids: list[str],
    user_link_repo: IUserLinkRepo = Depends(user_link_repo_depend),
):
    try:
        reorder_links_usecase = ReorderLinks(user_link_repo)
        outputs_list = await reorder_links_usecase.execute(user_id, link_ids)
        return [ output.model_dump(mode="json") for output in outputs_list ]
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
