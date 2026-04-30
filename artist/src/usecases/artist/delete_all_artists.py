from src.repo.interface.Iartist_repo import IArtistRepo
from src.repo.interface.Iartist_image_repo import IArtistImageRepo
from src.repo.interface.Iartist_link_repo import IArtistLinkRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteAllArtists:
    
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
    ) -> OperationOutput:
        
        try:
            status = await self.storage_repo.clean_dir()
            if status:
                await self.artist_image_repo.delete_all_images()
                await self.artist_link_repo.delete_all_links()
                status = await self.artist_repo.delete_all_artists()                    
            
            return OperationOutput(id=None, request="delete/all_artists", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  