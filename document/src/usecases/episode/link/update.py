from src.repo.interface.episode.Iepisode_link_repo import IEpisodeLinkRepo
from src.models.schemas.episode.update_link_input import UpdateLinkInput
from src.domain.schemas.episode.episode_link import EpisodeLinkModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class UpdateLink:
    
    def __init__(
        self,
        episode_link_repo: IEpisodeLinkRepo,
    ):

        self.episode_link_repo = episode_link_repo
    
    async def execute(
        self,
        entity: UpdateLinkInput,
    ) -> EpisodeLinkModel:
        
        try:
            link_model: EpisodeLinkModel = EpisodeLinkModel.model_validate(entity, from_attributes=True)            
            return await self.episode_link_repo.update(link_model)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  