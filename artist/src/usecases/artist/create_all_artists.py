from src.repo.interface.Iartist_repo import IArtistRepo
from src.models.schemas.artist.create_artist_input import CreateArtistInput
from src.domain.schemas.artist.artist_model import ArtistModel
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class CreateAllArtists:
    
    def __init__(
        self,
        artist_repo: IArtistRepo,
    ):
        
        self.artist_repo = artist_repo
    
    async def execute(
        self,
        artists: list[CreateArtistInput],
    ) -> ArtistModel:
        
        for artist in artists:
            
            try:
                artist = ArtistModel.model_validate(artist, from_attributes=True)
                await self.artist_repo.create_artist(artist)
            except AppBaseException:
                raise
            except:
                raise OperationFailureException(500, "Internal server error")
            
        return OperationOutput(id=None, request="create/all_artists", status=True)