from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.repo.interface.document.Idocument_repo import IDocumentRepo
from src.routes.depends.repo_depend import document_repo_depend
from src.repo.interface.document.Idocument_image_repo import IDocumentImageRepo
from src.routes.depends.repo_depend import document_image_repo_depend
from src.repo.interface.Istorage_repo import IStorageRepo
from src.routes.depends.storage_depend import storage_repo_depend
from src.usecases.document.image.delete_by_id import DeleteImage
from src.infra.exceptions.exceptions import AppBaseException

@router.delete(
    "/",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def delete_by_id(
    image_id: str = Query(...),
    document_repo: IDocumentRepo = Depends(document_repo_depend),
    document_image_repo: IDocumentImageRepo = Depends(document_image_repo_depend),
    storage_repo: IStorageRepo = Depends(storage_repo_depend),
):
    try:
        delete_image_usecase = DeleteImage(document_repo, document_image_repo, storage_repo)
        output = await delete_image_usecase.execute(image_id)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
