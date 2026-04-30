from ._router import router
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.repo.interface.document.Idocument_link_repo import IDocumentLinkRepo
from src.routes.depends.repo_depend import document_link_repo_depend
from src.usecases.document.link.reorder import ReorderLinks
from src.infra.exceptions.exceptions import AppBaseException

@router.put(
    "/reorder",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def reorder(
    document_id: str,
    link_ids: list[str],
    document_link_repo: IDocumentLinkRepo = Depends(document_link_repo_depend),
):
    try:
        reorder_links_usecase = ReorderLinks(document_link_repo)
        outputs_list = await reorder_links_usecase.execute(document_id, link_ids)
        return [ output.model_dump(mode="json") for output in outputs_list ]
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
