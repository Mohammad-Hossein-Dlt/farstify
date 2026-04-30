from ._router import router
from fastapi import Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.document.create_document_input import CreateDocumentInput
from src.repo.interface.document.Idocument_repo import IDocumentRepo
from src.routes.depends.repo_depend import document_repo_depend
from src.repo.interface.Istorage_repo import IStorageRepo
from src.routes.depends.storage_depend import storage_repo_depend
from src.usecases.document.management.create import CreateDocument
from src.infra.exceptions.exceptions import AppBaseException

@router.post(
    "/",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def create(
    entity: CreateDocumentInput = Query(...),
    document_repo: IDocumentRepo = Depends(document_repo_depend),
    storage_repo: IStorageRepo = Depends(storage_repo_depend),
):
    try:
        create_document_usecase = CreateDocument(document_repo, storage_repo)
        output = await create_document_usecase.execute(entity)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
