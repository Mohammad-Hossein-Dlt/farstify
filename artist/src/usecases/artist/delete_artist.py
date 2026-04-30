from src.repo.interface.Iartist_repo import IArtistRepo
from src.repo.interface.Iartist_image_repo import IArtistImageRepo
from src.repo.interface.Iartist_link_repo import IArtistLinkRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.domain.schemas.artist.artist_model import ArtistModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteArtist:
    
    def __init__(
        self,
        artist_repo: IArtistRepo,
        artist_image_repo: IArtistImageRepo,
        artist_link_repo: IArtistLinkRepo,
        storage_repo: IStorageRepo,
    ):
        
        self.artist_repo = artist_repo
        self.artist_image_repo = artist_image_repo
        self.artist_link_repo = artist_link_repo
        self.storage_repo = storage_repo
    
    async def execute(
        self,
        artist_id: str,
    ) -> OperationOutput:
        
        try:
            status = False
            artist: ArtistModel = await self.artist_repo.get_artist_by_id(artist_id)
            check_path = await self.storage_repo.path_objects(str(artist.id))
            if check_path:
                delete_objects = await self.storage_repo.delete_objects(str(artist.id))
                if delete_objects:
                    await self.artist_image_repo.delete_artist_images(artist_id)
                    await self.artist_link_repo.delete_artist_links(artist_id)
                    status = await self.artist_repo.delete_artist(artist_id)
            else:
                await self.artist_image_repo.delete_artist_images(artist_id)
                await self.artist_link_repo.delete_artist_links(artist_id)
                status = await self.artist_repo.delete_artist(artist_id)
            
            return OperationOutput(id=artist_id, request="delete/artist", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  