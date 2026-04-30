from ._router import router
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.repo.interface.Idocument_repo import IDocumentRepo
from src.routes.depends.repo_depend import document_repo_depend
from src.usecases.document.create_all import CreateAllDocuments
from data.documents import all_document
from src.infra.exceptions.exceptions import AppBaseException

@router.post(
    "/all",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def create_all(
    document_repo: IDocumentRepo = Depends(document_repo_depend),
):
    try:
        create_documents_usecase = CreateAllDocuments(document_repo)
        output = await create_documents_usecase.execute(all_document)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
