from src.repo.interface.user.Iuser_link_repo import IUserLinkRepo
from src.domain.schemas.user.user_link import UserLinkModel
from src.infra.database.mongodb.collections.user.user_link_collection import UserLinkCollection
from src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria
from src.infra.exceptions.exceptions import EntityNotFoundError
from src.infra.utils.convert_id import convert_object_id

class UserLinkMongodbRepo(IUserLinkRepo):
        
    async def create(
        self,
        link: UserLinkModel,
    ) -> UserLinkModel:
        
        new_link = await UserLinkCollection(
            **link.model_dump(exclude={"id", "_id"}),
        ).insert()
        return UserLinkModel.model_validate(new_link, from_attributes=True)
        
    async def get_by_id(
        self,
        link_id: str,
    ) -> UserLinkModel:
        
        try:
                                    
            link_id = convert_object_id(link_id)
            
            link = await UserLinkCollection.find_one(
                UserLinkCollection.id == link_id,
            )
                        
            return UserLinkModel.model_validate(link, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")

    async def update(
        self,
        link: UserLinkModel,
    ) -> UserLinkModel:
        
        try:               
            
            to_update: dict = link.custom_model_dump(
                exclude_none=True,
                db_stack="no-sql",
            )
            
            await UserLinkCollection.find(
                UserLinkCollection.id == link.id,
            ).update(
                {
                    "$set": to_update,
                },
            )
                        
            return await self.get_by_id(link.id)
        except EntityNotFoundError:
            raise
        
    async def delete_by_id(
        self,
        link_id: str,
    ) -> bool:
        
        try:
            link_id = convert_object_id(link_id)
            result = await UserLinkCollection.find(
                UserLinkCollection.id == link_id,
            ).delete()                       
            return bool(result.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")
        
    async def get_by_user_id(
        self,
        user_id: str,
        criteria: BaseFilterCriteria,
    ) -> list[UserLinkModel]:
        
        try:
            user_id = convert_object_id(user_id)
            links_list = await UserLinkCollection.find_many(
                UserLinkCollection.user_id == user_id,
            ).skip(
                criteria.page * criteria.limit
            ).limit(
                criteria.limit
            ).to_list()
            return [ UserLinkModel.model_validate(link, from_attributes=True) for link in links_list ]
        except EntityNotFoundError:
            raise EntityNotFoundError(status_code=404, message="There are no users")
    
    async def delete_by_user_id(
        self,
        user_id: str,
    ) -> bool:
        try:
            user_id = convert_object_id(user_id)
            result = await UserLinkCollection.find(
                UserLinkCollection.user_id == user_id
            ).delete()
            return bool(result.deleted_count) 
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")
    
    async def delete_all(
        self,
    ) -> bool:
        try:
            result = await UserLinkCollection.find_all().delete()
            return bool(result.deleted_count) 
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")
