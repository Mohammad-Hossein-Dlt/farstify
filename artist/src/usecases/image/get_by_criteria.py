from src.repo.interface.Iartist_repo import IArtistRepo
from src.repo.interface.Iartist_image_repo import IArtistImageRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.models.schemas.filter.sort_direction_filter_input import SortDirectionFilterInput
from src.domain.schemas.artist.artist_image import ArtistImageModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetAllImages:
    
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
        criteria: SortDirectionFilterInput,
    ) -> list[ArtistImageModel]:
        
        try:
            images: list[ArtistImageModel] = await self.artist_image_repo.get_by_artist_id(criteria.value)
            if isinstance(images, list):
                if criteria.order == "asc":
                    images.sort(key=lambda x: (x.order is None, x.order))
                elif criteria.order == "desc":
                    images.reverse()
                    images.sort(key=lambda x: (0 if x.order is None else 1, x.order), reverse=True)
            return images
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  