from src.repo.interface.user.Iuser_link_repo import IUserLinkRepo
from src.domain.schemas.user.user_link import UserLinkModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetLink:
    
    def __init__(
        self,
        user_link_repo: IUserLinkRepo,
    ):
        
        self.user_link_repo = user_link_repo
    
    async def execute(
        self,
        link_id: str,
    ) -> UserLinkModel:
        
        try:
            return await self.user_link_repo.get_by_id(link_id)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  