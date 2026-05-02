from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from document.src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria
from src.repo.interface.document.Idocument_link_repo import IDocumentLinkRepo
from src.routes.depends.repo_depend import document_link_repo_depend
from src.usecases.document.link.get_by_document_id import GetAllLinks
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
    document_link_repo: IDocumentLinkRepo = Depends(document_link_repo_depend),
):
    try:
        get_all_links_usecase = GetAllLinks(document_link_repo)
        outputs_list = await get_all_links_usecase.execute(document_id, criteria)
        return [ output.model_dump(mode="json") for output in outputs_list ]
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
