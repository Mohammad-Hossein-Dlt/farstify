from src.repo.interface.episode.Iepisode_image_repo import IEpisodeImageRepo
from src.domain.schemas.episode.episode_image import EpisodeImageModel
from src.infra.database.mongodb.collections.episode.episode_image_collection import EpisodeImageCollection
from src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria
from src.infra.exceptions.exceptions import EntityNotFoundError
from src.infra.utils.convert_id import convert_object_id

class EpisodeImageMongodbRepo(IEpisodeImageRepo):
        
    async def create(
        self,
        image: EpisodeImageModel,
    ) -> EpisodeImageModel:
        
        new_episode = await EpisodeImageCollection(
            **image.model_dump(exclude={"id", "_id"}),
        ).insert()
        return EpisodeImageModel.model_validate(new_episode, from_attributes=True)
        
    async def get_by_id(
        self,
        image_id: str,
    ) -> EpisodeImageModel:
        
        try:
                                    
            image_id = convert_object_id(image_id)
            
            image = await EpisodeImageCollection.find_one(
                EpisodeImageCollection.id == image_id,
            )
                        
            return EpisodeImageModel.model_validate(image, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="episode not found")

    async def update(
        self,
        image: EpisodeImageModel,
    ) -> EpisodeImageModel:
        
        try:               
            
            to_update: dict = image.custom_model_dump(
                exclude_none=True,
                db_stack="no-sql",
            )
            
            await EpisodeImageCollection.find(
                EpisodeImageCollection.id == image.id,
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
            result = await EpisodeImageCollection.find(
                EpisodeImageCollection.id == image_id,
            ).delete()                       
            return bool(result.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="episode not found")
        
    async def get_by_episode_id(
        self,
        episode_id: str,
        criteria: BaseFilterCriteria | None = None,
    ) -> list[EpisodeImageModel]:
        
        try:
            episode_id = convert_object_id(episode_id)
            query = EpisodeImageCollection.find_many(
                EpisodeImageCollection.episode_id == episode_id,
            )
            
            if criteria:
                query.skip(
                    criteria.page * criteria.limit
                ).limit(
                    criteria.limit
                ).sort(
                    EpisodeImageCollection.created_at if criteria.order == "asc" else -EpisodeImageCollection.created_at
                )
            
            images_list = await query.to_list()
                
            return [ EpisodeImageModel.model_validate(image, from_attributes=True) for image in images_list ]
        except EntityNotFoundError:
            raise EntityNotFoundError(status_code=404, message="There are no episodes")
    
    async def delete_by_episode_id(
        self,
        episode_id: str,
    ) -> bool:
        try:
            episode_id = convert_object_id(episode_id)
            result = await EpisodeImageCollection.find(
                EpisodeImageCollection.episode_id == episode_id
            ).delete()
            return bool(result.deleted_count) 
        except:
            raise EntityNotFoundError(status_code=404, message="episode not found")
    
    async def delete_all(
        self,
    ) -> bool:
        try:
            result = await EpisodeImageCollection.find_all().delete()
            return bool(result.deleted_count) 
        except:
            raise EntityNotFoundError(status_code=404, message="episode not found")
