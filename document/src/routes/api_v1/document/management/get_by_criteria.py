from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.filter.sort_direction_filter_input import SortDirectionFilterInput
from src.repo.interface.document.Idocument_repo import IDocumentRepo
from src.routes.depends.repo_depend import document_repo_depend
from src.usecases.document.management.get_by_criteria import GetAllDocuments
from src.infra.exceptions.exceptions import AppBaseException

@router.get(
    "/all",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def get_all_by_criteria(
    criteria: SortDirectionFilterInput = Query(...),
    document_repo: IDocumentRepo = Depends(document_repo_depend),
):
    try:
        get_all_documents_usecase = GetAllDocuments(document_repo)
        outputs_list = await get_all_documents_usecase.execute(criteria)
        return [ output.model_dump(mode="json") for output in outputs_list ]
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
