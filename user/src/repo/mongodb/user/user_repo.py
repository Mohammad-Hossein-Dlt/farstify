from src.repo.interface.user.Iuser_repo import IUserRepo
from src.domain.schemas.user.user_model import UserModel
from src.infra.database.mongodb.collections.user.user_collection import UserCollection
from src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria
from src.infra.exceptions.exceptions import EntityNotFoundError, DuplicateEntityError
from src.infra.utils.convert_id import convert_object_id

class UserMongodbRepo(IUserRepo):
        
    async def create(
        self,
        user: UserModel,
    ) -> UserModel:
        
        try:
            await self.get_by_name(user.name)
            raise DuplicateEntityError(409, "User already exist")
        except EntityNotFoundError:
            new_user = await UserCollection(
                **user.model_dump(exclude={"id", "_id"}),
            ).insert()
            return UserModel.model_validate(new_user, from_attributes=True)
    
    async def get_by_name(
        self,
        name: str,
    ) -> UserModel:
        
        try:
            result = await UserCollection.find_one(
                UserCollection.name == name,
            )
            return UserModel.model_validate(result, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")
        
    async def get_by_id(
        self,
        user_id: str,
    ) -> UserModel:
        
        try:
                                    
            user_id = convert_object_id(user_id)
            
            user = await UserCollection.find_one(
                UserCollection.id == user_id,
            )
                        
            return UserModel.model_validate(user, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")

    async def update(
        self,
        user: UserModel,
    ) -> UserModel:
        
        try:               
            
            to_update: dict = user.custom_model_dump(
                # exclude_unset=True,
                exclude_none=True,
                db_stack="no-sql",
            )
            
            await UserCollection.find(
                UserCollection.id == user.id,
            ).update(
                {
                    "$set": to_update,
                },
            )
                        
            return await self.get_by_id(user.id)
        except EntityNotFoundError:
            raise
        
    async def delete_by_id(
        self,
        user_id: str,
    ) -> bool:
        
        try:
            user_id = convert_object_id(user_id)
            delete_user = await UserCollection.find(
                UserCollection.id == user_id,
            ).delete()                       
            return bool(delete_user.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")
    
    async def get_all(
        self,
        criteria: BaseFilterCriteria | None = None,
    ) -> list[UserModel]:    
        try:
            query = UserCollection.find_all()
            
            if criteria:
                query.skip(
                    criteria.page * criteria.limit
                ).limit(
                    criteria.limit
                ).sort(
                    UserCollection.created_at if criteria.order == "asc" else -UserCollection.created_at
                )
            
            users_list = await query.to_list()
          
            return [ UserModel.model_validate(user, from_attributes=True) for user in users_list ]
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")
    
    async def delete_all(
        self,
    ) -> bool:
        try:
            delete_users = await UserCollection.delete_all()
            return bool(delete_users.deleted_count) 
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")
