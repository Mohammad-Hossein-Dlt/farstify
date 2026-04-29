from src.repo.interface.Iartist_repo import IArtistRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.models.schemas.artist.create_artist_input import CreateArtistInput
from src.domain.schemas.artist.artist_model import ArtistModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class CreateArtist:
    
    def __init__(
        self,
        artist_repo: IArtistRepo,
        storage_repo: IStorageRepo,
    ):
        
        self.artist_repo = artist_repo
        self.storage_repo = storage_repo
    
    async def execute(
        self,
        to_insert: CreateArtistInput,
    ) -> ArtistModel:
        
        try:
            artist: ArtistModel = ArtistModel.model_validate(to_insert, from_attributes=True)
            return await self.artist_repo.create_artist(artist)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  