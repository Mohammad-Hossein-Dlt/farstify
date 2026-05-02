from src.repo.interface.Iuser_link_repo import IUserLinkRepo
from user.src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria
from src.domain.schemas.user.user_link import UserLinkModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetAllLinks:
    
    def __init__(
        self,
        user_link_repo: IUserLinkRepo,
    ):
        
        self.user_link_repo = user_link_repo
    
    async def execute(
        self,
        user_id: str,
        criteria: BaseFilterCriteria,
    ) -> list[UserLinkModel]:
        
        try:
            links: list[BaseFilterCriteria] = await self.user_link_repo.get_by_user_id(user_id, criteria)
            if isinstance(links, list):
                if criteria.order == "asc":
                    links.sort(key=lambda x: (x.order is None, x.order))
                elif criteria.order == "desc":
                    links.reverse()
                    links.sort(key=lambda x: (0 if x.order is None else 1, x.order), reverse=True)
            return links
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  