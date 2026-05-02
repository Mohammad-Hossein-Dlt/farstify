from src.repo.interface.user.Iuser_repo import IUserRepo
from src.repo.interface.user.Iuser_image_repo import IUserImageRepo
from src.repo.interface.Istorage_repo import IStorageRepo
from src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria
from src.domain.schemas.user.user_image import UserImageModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetAllImages:
    
    def __init__(
        self,
        user_repo: IUserRepo,
        user_image_repo: IUserImageRepo,
        storage_repo: IStorageRepo,
    ):
        
        self.user_repo = user_repo
        self.user_image_repo = user_image_repo
        self.storage_repo = storage_repo
    
    async def execute(
        self,
        user_id: str,
        criteria: BaseFilterCriteria,
    ) -> list[UserImageModel]:
        
        try:
            images: list[UserImageModel] = await self.user_image_repo.get_by_user_id(user_id, criteria)
            if isinstance(images, list):
                if criteria.order == "asc":
                    images.sort(key=lambda x: (x.order is None, x.order))
                elif criteria.order == "desc":
                    images.reverse()
                    images.sort(key=lambda x: (0 if x.order is None else 1, x.order), reverse=True)
            return images
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  