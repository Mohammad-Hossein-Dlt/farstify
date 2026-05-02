from src.repo.interface.Iuser_link_repo import IUserLinkRepo
from src.domain.schemas.user.user_link import UserLinkModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class ReorderLinks:
    
    def __init__(
        self,
        user_link_repo: IUserLinkRepo,
    ):

        self.user_link_repo = user_link_repo
    
    async def execute(
        self,
        user_id: str,
        link_ids: list[str],
    ) -> list[UserLinkModel]:
        
        try:
            links_list: list[UserLinkModel] = await self.user_link_repo.get_by_user_id(user_id)
            for index, links_id in enumerate(link_ids):
                for link in links_list:
                    if str(link.id) == links_id:
                        link.order = index
                        await self.user_link_repo.update(link)

            return await self.user_link_repo.get_by_user_id(user_id)        
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  