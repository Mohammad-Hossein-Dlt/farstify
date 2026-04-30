from src.repo.interface.Iartist_repo import IArtistRepo
from src.repo.interface.Iartist_image_repo import IArtistImageRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.domain.schemas.artist.artist_model import ArtistModel
from src.domain.schemas.artist.artist_image import ArtistImageModel
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteImage:
    
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
        image_id: str,
    ) -> OperationOutput:
        
        try:
            
            image: ArtistImageModel = await self.artist_image_repo.get_by_id(image_id)
            artist: ArtistModel = await self.artist_repo.get_by_id(image.artist_id)
            
            result = await self.storage_repo.delete_object(f"{artist.id}/" + image.cover)
            
            status = False
            if result:
                status = await self.artist_image_repo.delete_by_id(image.id)

            return OperationOutput(id=image_id, request="delete/artist-image", status=status)
        
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  