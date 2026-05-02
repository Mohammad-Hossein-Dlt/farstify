from src.repo.interface.Iuser_repo import IUserRepo
from src.repo.interface.Iuser_link_repo import IUserLinkRepo
from src.models.schemas.user.create_link_input import CreateLinkInput
from src.domain.schemas.user.user_link import UserLinkModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class CreateLink:
    
    def __init__(
        self,
        user_repo: IUserRepo,
        user_link_repo: IUserLinkRepo,
    ):
        
        self.user_repo = user_repo
        self.user_link_repo = user_link_repo
    
    async def execute(
        self,
        entity: CreateLinkInput,
    ) -> UserLinkModel:
        
        try:
            await self.user_repo.get_by_id(entity.user_id)
            link_model: UserLinkModel = UserLinkModel.model_validate(entity, from_attributes=True)
            return await self.user_link_repo.create(link_model)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  