from ._router import router
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.repo.interface.document.Idocument_repo import IDocumentRepo
from src.routes.depends.repo_depend import document_repo_depend
from src.repo.interface.document.Idocument_image_repo import IDocumentImageRepo
from src.routes.depends.repo_depend import document_image_repo_depend
from src.usecases.document.image.reorder import ReorderImages
from src.infra.exceptions.exceptions import AppBaseException

@router.put(
    "/reorder",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def reorder(
    document_id: str,
    image_ids: list[str],
    document_repo: IDocumentRepo = Depends(document_repo_depend),
    document_image_repo: IDocumentImageRepo = Depends(document_image_repo_depend),
):
    try:
        reorder_images_usecase = ReorderImages(document_repo, document_image_repo)
        outputs_list = await reorder_images_usecase.execute(document_id, image_ids)
        return [ output.model_dump(mode="json") for output in outputs_list ]
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
