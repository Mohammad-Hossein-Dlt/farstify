from src.repo.interface.Iartist_repo import IArtistRepo
from src.repo.interface.Iartist_image_repo import IArtistImageRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.domain.schemas.artist.artist_model import ArtistModel
from src.domain.schemas.artist.artist_image import ArtistImageModel
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteAllImages:
    
    def __init__(
        self,
        artist_repo: IArtistRepo,
        artist_image_repo: IArtistImageRepo,
        storage_repo: IStorageRepo,
    ):
        
        self.artist_repo = artist_repo
        self.artist_image_repo = artist_image_repo
        self.storage_repo = storage_repo
    
    async def execute(
        self,
        artist_id: str,
    ) -> OperationOutput:
        
        try:
            artist: ArtistModel = await self.artist_repo.get_by_id(artist_id)
            images: list[ArtistImageModel] = await self.artist_image_repo.get_by_artist_id(artist_id)
            
            status = True if images else False
            for i in images:
                result = await self.storage_repo.delete_object(f"{artist.id}/" + i.cover)
                if result:
                    await self.artist_image_repo.delete_by_id(i.id)
                else:
                    status = False
            
            return OperationOutput(id=artist_id, request="delete/all-artist-images", status=status)        
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  