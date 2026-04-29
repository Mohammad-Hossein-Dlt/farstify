from ._router import router
from fastapi import Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.artist.create_link_input import CreateLinkInput
from src.repo.interface.Iartist_repo import IArtistRepo
from src.routes.depends.repo_depend import artist_repo_depend
from src.repo.interface.Iartist_link_repo import IArtistLinkRepo
from src.routes.depends.repo_depend import artist_link_repo_depend
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
    artist_repo: IArtistRepo = Depends(artist_repo_depend),
    artist_link_repo: IArtistLinkRepo = Depends(artist_link_repo_depend),
):
    try:
        create_link_usecase = CreateLink(artist_repo, artist_link_repo)
        output = await create_link_usecase.execute(link)            
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
