from src.repo.interface.Iartist_repo import IArtistRepo
from src.repo.interface.Iartist_image_repo import IArtistImageRepo
from src.domain.schemas.artist.artist_image import ArtistImageModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class ReorderImages:
    
    def __init__(
        self,
        artist_repo: IArtistRepo,
        artist_image_repo: IArtistImageRepo,
    ):
        
        self.artist_repo = artist_repo
        self.artist_image_repo = artist_image_repo
    
    async def execute(
        self,
        artist_id: str,
        image_ids: list[str],
    ) -> list[ArtistImageModel]:
        
        try:
            images_list: list[ArtistImageModel] = await self.artist_image_repo.get_images(artist_id)
            for index, image_id in enumerate(image_ids):
                for image in images_list:
                    if str(image.id) == image_id:
                        image.order = index
                        await self.artist_image_repo.update_image(image)

            return await self.artist_image_repo.get_images(artist_id)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  