from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.repo.interface.Idocument_repo import IDocumentRepo
from src.routes.depends.repo_depend import document_repo_depend
from src.usecases.document.get_document import GetDocument
from src.infra.exceptions.exceptions import AppBaseException

@router.get(
    "/",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def get_document(
    document_id: str = Query(...),
    document_repo: IDocumentRepo = Depends(document_repo_depend),
):
    try:
        get_document_usecase = GetDocument(document_repo)
        output = await get_document_usecase.execute(document_id)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
