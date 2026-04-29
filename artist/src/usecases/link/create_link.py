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
        to_create: CreateLinkInput,
    ) -> ArtistLinkModel:
        
        try:
            await self.artist_repo.get_artist_by_id(to_create.artist_id)
            link_model: ArtistLinkModel = ArtistLinkModel.model_validate(to_create, from_attributes=True)
            return await self.artist_link_repo.create_link(link_model)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  