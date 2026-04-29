from src.repo.interface.Iartist_repo import IArtistRepo
from src.repo.interface.Iartist_image_repo import IArtistImageRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.domain.schemas.artist.artist_image import ArtistImageModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetImage:
    
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
    ) -> ArtistImageModel:
        
        try:
            return await self.artist_image_repo.get_image_by_id(image_id)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  