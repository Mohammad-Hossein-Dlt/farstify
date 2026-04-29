from src.repo.interface.Iartist_repo import IArtistRepo
from src.models.schemas.filter.sort_direction_filter_input import SortDirectionFilterInput
from src.domain.schemas.artist.artist_model import ArtistModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetAllArtists:
    
    def __init__(
        self,
        artist_repo: IArtistRepo,
    ):
        
        self.artist_repo = artist_repo  
    
    async def execute(
        self,
        to_filter: SortDirectionFilterInput,
    ) -> list[ArtistModel]:
        
        try:
            artists: list[ArtistModel] = await self.artist_repo.get_all_artists()
            if isinstance(artists, list):
                if to_filter.order == "asc":
                    pass
                elif to_filter.order == "desc":
                    artists.reverse()
            return artists
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  