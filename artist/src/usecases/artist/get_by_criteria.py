from src.repo.interface.Iartist_repo import IArtistRepo
from src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria
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
        criteria: BaseFilterCriteria,
    ) -> list[ArtistModel]:
        
        try:
            artists: list[ArtistModel] = await self.artist_repo.get_all(criteria)
            if isinstance(artists, list):
                if criteria.order == "asc":
                    pass
                elif criteria.order == "desc":
                    artists.reverse()
            return artists
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  