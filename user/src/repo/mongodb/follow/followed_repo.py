from src.repo.interface.follow.Ifollow_repo import IFollowRepo, FollowModel
from src.domain.schemas.follow.follow_model import FollowModel
from src.infra.database.mongodb.collections.follow.follows import FollowsCollection
from src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria
from src.infra.exceptions.exceptions import EntityNotFoundError
from src.infra.utils.convert_id import convert_object_id
from beanie.operators import And

class FollowMongodbRepo(IFollowRepo):
                
    async def create(
        self,
        follow: FollowModel,
    ) -> FollowModel:
        
        try:
            new_user = await FollowsCollection(
                **follow.model_dump(exclude={"id", "_id"}),
            ).insert()
            return FollowModel.model_validate(new_user, from_attributes=True)
        except:
            ...
    
    async def check_unique(
        self,
        follow: FollowModel,
    ) -> FollowModel:
        
        try:
            follow = await FollowsCollection.find_one(
                And(
                    FollowsCollection.user_id == follow.user_id,
                    FollowsCollection.target_id == follow.target_id,
                )
            )
                        
            return FollowModel.model_validate(follow, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")
        
    async def get_by_id(
        self,
        follow_id: str,
    ) -> FollowModel:
        
        try:
            follow_id = convert_object_id(follow_id)
            follow = await FollowsCollection.find_one(
                FollowsCollection.id == follow_id,
            )
                        
            return FollowModel.model_validate(follow, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")

    async def update(
        self,
        follow: FollowModel,
    ) -> FollowModel:
        
        try:               
            to_update: dict = follow.custom_model_dump(
                exclude_none=True,
                db_stack="no-sql",
            )
            
            await FollowsCollection.find(
                FollowsCollection.id == follow.id,
            ).update(
                {
                    "$set": to_update,
                },
            )
                                    
            return await self.get_by_id(follow.id)
        except EntityNotFoundError:
            raise
        
    async def delete_by_id(
        self,
        follow_id: str,
    ) -> bool:
        
        try:
            follow_id = convert_object_id(follow_id)
            result = await FollowsCollection.find(
                FollowsCollection.id == follow_id,
            ).delete()                       
            return bool(result.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")
        
    async def get_by_user_id(
        self,
        user_id: str,
        criteria: BaseFilterCriteria,
    ) -> list[FollowModel]:
        
        try:
            user_id = convert_object_id(user_id)
            follows_list = await FollowsCollection.find_many(
                FollowsCollection.user_id == user_id,
            ).skip(
                criteria.page * criteria.limit
            ).limit(
                criteria.limit
            ).sort(
                FollowsCollection.created_at if criteria.order == "asc" else -FollowsCollection.created_at
            ).to_list()
            return [ FollowModel.model_validate(follow, from_attributes=True) for follow in follows_list ]
        except EntityNotFoundError:
            raise EntityNotFoundError(status_code=404, message="There are no users")
    
    async def delete_by_user_id(
        self,
        user_id: str,
    ) -> bool:
        try:
            user_id = convert_object_id(user_id)
            result = await FollowsCollection.find(
                FollowsCollection.user_id == user_id
            ).delete()
            return bool(result.deleted_count) 
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")
    
    async def delete_all(
        self,
    ) -> bool:
        try:
            result = await FollowsCollection.find_all().delete()
            return bool(result.deleted_count) 
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")
