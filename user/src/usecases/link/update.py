from src.repo.interface.user.Iuser_link_repo import IUserLinkRepo
from src.models.schemas.user.update_link_input import UpdateLinkInput
from src.domain.schemas.user.user_link import UserLinkModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class UpdateLink:
    
    def __init__(
        self,
        user_link_repo: IUserLinkRepo,
    ):

        self.user_link_repo = user_link_repo
    
    async def execute(
        self,
        entity: UpdateLinkInput,
    ) -> UserLinkModel:
        
        try:
            link_model: UserLinkModel = UserLinkModel.model_validate(entity, from_attributes=True)            
            return await self.user_link_repo.update(link_model)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  