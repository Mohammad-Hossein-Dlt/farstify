from ._router import router
from fastapi import Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.document.update_link_input import UpdateLinkInput
from src.repo.interface.Idocument_link_repo import IDocumentLinkRepo
from src.routes.depends.repo_depend import document_link_repo_depend
from src.usecases.link.update_link import UpdateLink
from src.infra.exceptions.exceptions import AppBaseException

@router.put(
    "/",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def update_link(
    link: UpdateLinkInput = Query(...),
    document_link_repo: IDocumentLinkRepo = Depends(document_link_repo_depend),
):
    try:
        update_link_usecase = UpdateLink(document_link_repo)
        output = await update_link_usecase.execute(link)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
