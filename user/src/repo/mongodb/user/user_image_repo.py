from src.repo.interface.user.Iuser_image_repo import IUserImageRepo
from src.domain.schemas.user.user_image import UserImageModel
from src.infra.database.mongodb.collections.user.user_image_collection import UserImageCollection
from src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria
from src.infra.exceptions.exceptions import EntityNotFoundError
from src.infra.utils.convert_id import convert_object_id

class UserImageMongodbRepo(IUserImageRepo):
        
    async def create(
        self,
        image: UserImageModel,
    ) -> UserImageModel:
        
        new_user = await UserImageCollection(
            **image.model_dump(exclude={"id", "_id"}),
        ).insert()
        return UserImageModel.model_validate(new_user, from_attributes=True)
        
    async def get_by_id(
        self,
        image_id: str,
    ) -> UserImageModel:
        
        try:
                                    
            image_id = convert_object_id(image_id)
            
            image = await UserImageCollection.find_one(
                UserImageCollection.id == image_id,
            )
                        
            return UserImageModel.model_validate(image, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")

    async def update(
        self,
        image: UserImageModel,
    ) -> UserImageModel:
        
        try:               
            
            to_update: dict = image.custom_model_dump(
                exclude_none=True,
                db_stack="no-sql",
            )
            
            await UserImageCollection.find(
                UserImageCollection.id == image.id,
            ).update(
                {
                    "$set": to_update,
                },
            )
                                    
            return await self.get_by_id(image.id)
        except EntityNotFoundError:
            raise
        
    async def delete_by_id(
        self,
        image_id: str,
    ) -> bool:
        
        try:
            image_id = convert_object_id(image_id)
            result = await UserImageCollection.find(
                UserImageCollection.id == image_id,
            ).delete()                       
            return bool(result.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")
        
    async def get_by_user_id(
        self,
        user_id: str,
        criteria: BaseFilterCriteria,
    ) -> list[UserImageModel]:
        
        try:
            user_id = convert_object_id(user_id)
            images_list = await UserImageCollection.find_many(
                UserImageCollection.user_id == user_id,
            ).skip(
                criteria.page * criteria.limit
            ).limit(
                criteria.limit
            ).to_list()       
            return [ UserImageModel.model_validate(image, from_attributes=True) for image in images_list ]
        except EntityNotFoundError:
            raise EntityNotFoundError(status_code=404, message="There are no users")
    
    async def delete_by_user_id(
        self,
        user_id: str,
    ) -> bool:
        try:
            user_id = convert_object_id(user_id)
            result = await UserImageCollection.find(
                UserImageCollection.user_id == user_id
            ).delete()
            return bool(result.deleted_count) 
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")
    
    async def delete_all(
        self,
    ) -> bool:
        try:
            result = await UserImageCollection.find_all().delete()
            return bool(result.deleted_count) 
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")
