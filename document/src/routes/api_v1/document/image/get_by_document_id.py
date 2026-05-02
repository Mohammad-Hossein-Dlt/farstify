from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from document.src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria
from src.repo.interface.document.Idocument_repo import IDocumentRepo
from src.routes.depends.repo_depend import document_repo_depend
from src.repo.interface.document.Idocument_image_repo import IDocumentImageRepo
from src.routes.depends.repo_depend import document_image_repo_depend
from src.repo.interface.Istorage_repo import IStorageRepo
from src.routes.depends.storage_depend import storage_repo_depend
from src.usecases.document.image.get_by_document_id import GetAllImages
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
    document_repo: IDocumentRepo = Depends(document_repo_depend),
    document_image_repo: IDocumentImageRepo = Depends(document_image_repo_depend),
    storage_repo: IStorageRepo = Depends(storage_repo_depend),
):
    try:
        get_all_images_usecase = GetAllImages(document_repo, document_image_repo, storage_repo)
        outputs_list = await get_all_images_usecase.execute(document_id, criteria)
        return [ output.model_dump(mode="json") for output in outputs_list ]
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
