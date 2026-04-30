from ._router import router
from fastapi import Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.document.create_link_input import CreateLinkInput
from src.repo.interface.Idocument_repo import IDocumentRepo
from src.routes.depends.repo_depend import document_repo_depend
from src.repo.interface.Idocument_link_repo import IDocumentLinkRepo
from src.routes.depends.repo_depend import document_link_repo_depend
from src.usecases.link.create_link import CreateLink
from src.infra.exceptions.exceptions import AppBaseException

@router.post(
    "/",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def create_link(
    link: CreateLinkInput = Query(...),
    document_repo: IDocumentRepo = Depends(document_repo_depend),
    document_link_repo: IDocumentLinkRepo = Depends(document_link_repo_depend),
):
    try:
        create_link_usecase = CreateLink(document_repo, document_link_repo)
        output = await create_link_usecase.execute(link)            
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
