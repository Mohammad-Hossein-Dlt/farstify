from src.repo.interface.user.Iuser_repo import IUserRepo
from src.repo.interface.user.Iuser_image_repo import IUserImageRepo
from src.domain.schemas.user.user_image import UserImageModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class ReorderImages:
    
    def __init__(
        self,
        user_repo: IUserRepo,
        user_image_repo: IUserImageRepo,
    ):
        
        self.user_repo = user_repo
        self.user_image_repo = user_image_repo
    
    async def execute(
        self,
        user_id: str,
        image_ids: list[str],
    ) -> list[UserImageModel]:
        
        try:
            images_list: list[UserImageModel] = await self.user_image_repo.get_by_user_id(user_id)
            for index, image_id in enumerate(image_ids):
                for image in images_list:
                    if str(image.id) == image_id:
                        image.order = index
                        await self.user_image_repo.update(image)

            return await self.user_image_repo.get_by_user_id(user_id)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  