from src.repo.interface.Iartist_repo import IArtistRepo
from src.repo.interface.Iartist_link_repo import IArtistLinkRepo
from src.models.schemas.artist.create_link_input import CreateLinkInput
from src.domain.schemas.artist.artist_link import ArtistLinkModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class CreateLink:
    
    def __init__(
        self,
        artist_repo: IArtistRepo,
        artist_link_repo: IArtistLinkRepo,
    ):
        
        self.artist_repo = artist_repo
        self.artist_link_repo = artist_link_repo
    
    async def execute(
        self,
        entity: CreateLinkInput,
    ) -> ArtistLinkModel:
        
        try:
            await self.artist_repo.get_by_id(entity.artist_id)
            link_model: ArtistLinkModel = ArtistLinkModel.model_validate(entity, from_attributes=True)
            return await self.artist_link_repo.create(link_model)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  