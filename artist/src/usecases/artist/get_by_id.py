from src.repo.interface.Iartist_repo import IArtistRepo
from src.domain.schemas.artist.artist_model import ArtistModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetArtist:
    
    def __init__(
        self,
        artist_repo: IArtistRepo,
    ):
        
        self.artist_repo = artist_repo  
    
    async def execute(
        self,
        artist_id: str,
    ) -> ArtistModel:
        
        try:
            return await self.artist_repo.get_by_id(artist_id)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")