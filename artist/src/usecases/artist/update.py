from src.repo.interface.Iartist_repo import IArtistRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.models.schemas.artist.update_artist_input import UpdateArtistInput
from src.domain.schemas.artist.artist_model import ArtistModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class UpdateArtist:
    
    def __init__(
        self,
        artist_repo: IArtistRepo,
        storage_repo: IStorageRepo,
    ):
        
        self.artist_repo = artist_repo  
        self.storage_repo = storage_repo
    
    async def execute(
        self,
        entity: UpdateArtistInput,
    ) -> ArtistModel:
        
        try:
            artist_model: ArtistModel = ArtistModel.model_validate(entity, from_attributes=True)
            return await self.artist_repo.update(artist_model)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")