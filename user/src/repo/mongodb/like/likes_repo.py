from src.repo.interface.like.Ilikes_repo import ILikesRepo, LikeModel
from src.domain.schemas.like.like_model import LikeModel
from src.infra.database.mongodb.collections.like.likes_collection import LikesCollection
from src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria
from src.infra.exceptions.exceptions import EntityNotFoundError
from src.infra.utils.convert_id import convert_object_id
from beanie.operators import And

class LikeMongodbRepo(ILikesRepo):
                
    async def create(
        self,
        like: LikeModel,
    ) -> LikeModel:
        
        try:
            new_user = await LikesCollection(
                **like.model_dump(exclude={"id", "_id"}),
            ).insert()
            return LikeModel.model_validate(new_user, from_attributes=True)
        except:
            ...
    
    async def check_unique(
        self,
        like: LikeModel,
    ) -> LikeModel:
        
        try:
            like = await LikesCollection.find_one(
                And(
                    LikesCollection.user_id == like.user_id,
                    LikesCollection.episode_id == like.episode_id,
                )
            )
                        
            return LikeModel.model_validate(like, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="Like not found")
        
    async def get_by_id(
        self,
        like_id: str,
    ) -> LikeModel:
        
        try:
            like_id = convert_object_id(like_id)
            like = await LikesCollection.find_one(
                LikesCollection.id == like_id,
            )
                        
            return LikeModel.model_validate(like, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="Like not found")

    async def update(
        self,
        like: LikeModel,
    ) -> LikeModel:
        
        try:               
            to_update: dict = like.custom_model_dump(
                exclude_none=True,
                db_stack="no-sql",
            )
            
            await LikesCollection.find(
                LikesCollection.id == like.id,
            ).update(
                {
                    "$set": to_update,
                },
            )
                                    
            return await self.get_by_id(like.id)
        except EntityNotFoundError:
            raise
        
    async def delete_by_id(
        self,
        like_id: str,
    ) -> bool:
        
        try:
            like_id = convert_object_id(like_id)
            result = await LikesCollection.find(
                LikesCollection.id == like_id,
            ).delete()                       
            return bool(result.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="Like not found")
        
    async def get_by_user_id(
        self,
        user_id: str,
        criteria: BaseFilterCriteria | None = None,
    ) -> list[LikeModel]:
        
        try:
            user_id = convert_object_id(user_id)
            query = LikesCollection.find_many(
                LikesCollection.user_id == user_id,
            )
            
            if criteria:
                query.skip(
                    criteria.page * criteria.limit
                ).limit(
                    criteria.limit
                ).sort(
                    LikesCollection.created_at if criteria.order == "asc" else -LikesCollection.created_at
                )
            
            likes_list = await query.to_list()
            
            return [ LikeModel.model_validate(like, from_attributes=True) for like in likes_list ]
        except EntityNotFoundError:
            raise EntityNotFoundError(status_code=404, message="There are no likes")
    
    async def delete_by_user_id(
        self,
        user_id: str,
    ) -> bool:
        try:
            user_id = convert_object_id(user_id)
            result = await LikesCollection.find(
                LikesCollection.user_id == user_id
            ).delete()
            return bool(result.deleted_count) 
        except:
            raise EntityNotFoundError(status_code=404, message="Like not found")
    
    async def delete_all(
        self,
    ) -> bool:
        try:
            result = await LikesCollection.find_all().delete()
            return bool(result.deleted_count) 
        except:
            raise EntityNotFoundError(status_code=404, message="Like not found")
