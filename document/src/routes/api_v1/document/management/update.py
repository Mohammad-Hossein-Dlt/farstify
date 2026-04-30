from ._router import router
from fastapi import Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.document.update_document_input import UpdateDocumentInput
from src.repo.interface.document.Idocument_repo import IDocumentRepo
from src.routes.depends.repo_depend import document_repo_depend
from src.repo.interface.Istorage_repo import IStorageRepo
from src.routes.depends.storage_depend import storage_repo_depend
from src.usecases.document.management.update import UpdateDocument
from src.infra.exceptions.exceptions import AppBaseException

@router.put(
    "/",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def update(
    entity: UpdateDocumentInput = Query(...),
    document_repo: IDocumentRepo = Depends(document_repo_depend),
    storage_repo: IStorageRepo = Depends(storage_repo_depend),
):
    try:        
        update_document_usecase = UpdateDocument(document_repo, storage_repo)
        output = await update_document_usecase.execute(entity)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
