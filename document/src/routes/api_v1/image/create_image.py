from ._router import router
from fastapi import UploadFile, Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.document.create_image_input import CreateImageInput
from src.repo.interface.Idocument_repo import IDocumentRepo
from src.routes.depends.repo_depend import document_repo_depend
from src.repo.interface.Idocument_image_repo import IDocumentImageRepo
from src.routes.depends.repo_depend import document_image_repo_depend
from src.repo.interface.Istorage_repo import IStorageRepo
from src.routes.depends.storage_depend import storage_repo_depend
from src.usecases.image.create_image import CreateImage
from src.infra.exceptions.exceptions import AppBaseException

@router.post(
    "/",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def create_image(
    file: UploadFile | None = None,
    image: CreateImageInput = Query(...),
    document_repo: IDocumentRepo = Depends(document_repo_depend),
    document_image_repo: IDocumentImageRepo = Depends(document_image_repo_depend),
    storage_repo: IStorageRepo = Depends(storage_repo_depend),
):
    try:
        
        create_image_usecase = CreateImage(document_repo, document_image_repo, storage_repo)
        
        if file:
            output = await create_image_usecase.execute(
                image,
                file.file,
                file.filename,
                file.size,
                file.content_type,
            )
        else:
            output = await create_image_usecase.execute(image)
            
        return output.model_dump(mode="json")
    
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
