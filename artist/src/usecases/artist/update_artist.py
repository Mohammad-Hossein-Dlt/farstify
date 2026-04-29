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
        to_update: UpdateArtistInput,
    ) -> ArtistModel:
        
        try:
            artist: ArtistModel = ArtistModel.model_validate(to_update, from_attributes=True)
            return await self.artist_repo.update_artist(artist)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")