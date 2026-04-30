from ._router import router
from fastapi import UploadFile, Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.document.update_image_input import UpdateImageInput
from src.repo.interface.document.Idocument_repo import IDocumentRepo
from src.routes.depends.repo_depend import document_repo_depend
from src.repo.interface.document.Idocument_image_repo import IDocumentImageRepo
from src.routes.depends.repo_depend import document_image_repo_depend
from src.repo.interface.Istorage_repo import IStorageRepo
from src.routes.depends.storage_depend import storage_repo_depend
from src.usecases.document.image.update import UpdateImage
from src.infra.exceptions.exceptions import AppBaseException

@router.put(
    "/",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def update(
    file: UploadFile | None = None,
    entity: UpdateImageInput = Query(...),
    document_repo: IDocumentRepo = Depends(document_repo_depend),
    document_image_repo: IDocumentImageRepo = Depends(document_image_repo_depend),
    storage_repo: IStorageRepo = Depends(storage_repo_depend),
):
    try:
        
        update_image_usecase = UpdateImage(document_repo, document_image_repo, storage_repo)
        
        if file:
            output = await update_image_usecase.execute(
                entity,
                file.file,
                file.filename,
                file.size,
                file.content_type,
            )
        else:
            output = await update_image_usecase.execute(entity)
        
        return output.model_dump(mode="json")
    
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
