from ._router import router
from fastapi import UploadFile, Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.artist.update_image_input import UpdateImageInput
from src.repo.interface.Iartist_repo import IArtistRepo
from src.routes.depends.repo_depend import artist_repo_depend
from src.repo.interface.Iartist_image_repo import IArtistImageRepo
from src.routes.depends.repo_depend import artist_image_repo_depend
from src.repo.interface.Istorage_repo import IStorageRepo
from src.routes.depends.storage_depend import storage_repo_depend
from src.usecases.image.update_image import UpdateImage
from src.infra.exceptions.exceptions import AppBaseException

@router.put(
    "/",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def update_image(
    file: UploadFile | None = None,
    image: UpdateImageInput = Query(...),
    artist_repo: IArtistRepo = Depends(artist_repo_depend),
    artist_image_repo: IArtistImageRepo = Depends(artist_image_repo_depend),
    storage_repo: IStorageRepo = Depends(storage_repo_depend),
):
    try:
        
        update_image_usecase = UpdateImage(artist_repo, artist_image_repo, storage_repo)
        
        if file:
            output = await update_image_usecase.execute(
                image,
                file.file,
                file.filename,
                file.size,
                file.content_type,
            )
        else:
            output = await update_image_usecase.execute(image)
        
        return output.model_dump(mode="json")
    
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
