from src.repo.interface.episode.Iepisode_repo import IEpisodeRepo
from src.repo.interface.episode.Iepisode_link_repo import IEpisodeLinkRepo
from src.models.schemas.episode.create_link_input import CreateLinkInput
from src.domain.schemas.episode.episode_link import EpisodeLinkModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class CreateLink:
    
    def __init__(
        self,
        episode_repo: IEpisodeRepo,
        episode_link_repo: IEpisodeLinkRepo,
    ):
        
        self.episode_repo = episode_repo
        self.episode_link_repo = episode_link_repo
    
    async def execute(
        self,
        entity: CreateLinkInput,
    ) -> EpisodeLinkModel:
        
        try:
            await self.episode_repo.get_by_id(entity.episode_id)
            link_model: EpisodeLinkModel = EpisodeLinkModel.model_validate(entity, from_attributes=True)
            return await self.episode_link_repo.create(link_model)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  