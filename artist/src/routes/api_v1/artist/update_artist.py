from ._router import router
from fastapi import Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.artist.update_artist_input import UpdateArtistInput
from src.repo.interface.Iartist_repo import IArtistRepo
from src.routes.depends.repo_depend import artist_repo_depend
from src.repo.interface.Istorage_repo import IStorageRepo
from src.routes.depends.storage_depend import storage_repo_depend
from src.usecases.artist.update_artist import UpdateArtist
from src.infra.exceptions.exceptions import AppBaseException

@router.put(
    "/",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def update_artist(
    artist: UpdateArtistInput = Query(...),
    artist_repo: IArtistRepo = Depends(artist_repo_depend),
    storage_repo: IStorageRepo = Depends(storage_repo_depend),
):
    try:        
        update_artist_usecase = UpdateArtist(artist_repo, storage_repo)
        output = await update_artist_usecase.execute(artist)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
