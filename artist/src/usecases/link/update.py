from src.repo.interface.Iartist_link_repo import IArtistLinkRepo
from src.models.schemas.artist.update_link_input import UpdateLinkInput
from src.domain.schemas.artist.artist_link import ArtistLinkModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class UpdateLink:
    
    def __init__(
        self,
        artist_link_repo: IArtistLinkRepo,
    ):

        self.artist_link_repo = artist_link_repo
    
    async def execute(
        self,
        entity: UpdateLinkInput,
    ) -> ArtistLinkModel:
        
        try:
            link_model: ArtistLinkModel = ArtistLinkModel.model_validate(entity, from_attributes=True)            
            return await self.artist_link_repo.update(link_model)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  