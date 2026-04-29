from ._router import router
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.repo.interface.Iartist_repo import IArtistRepo
from src.routes.depends.repo_depend import artist_repo_depend
from src.usecases.artist.create_all_artists import CreateAllArtists
from data.artists import all_artist
from src.infra.exceptions.exceptions import AppBaseException

@router.post(
    "/all",
    status_code=201,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def create_artists(
    artist_repo: IArtistRepo = Depends(artist_repo_depend),
):
    try:
        create_artists_usecase = CreateAllArtists(artist_repo)
        output = await create_artists_usecase.execute(all_artist)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
