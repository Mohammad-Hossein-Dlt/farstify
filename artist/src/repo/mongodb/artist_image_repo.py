from src.repo.interface.Iartist_image_repo import IArtistImageRepo
from src.domain.schemas.artist.artist_image import ArtistImageModel
from src.infra.database.mongodb.collections.artist_image_collection import ArtistImageCollection
from src.infra.exceptions.exceptions import EntityNotFoundError
from src.infra.utils.convert_id import convert_object_id

class ArtistImageMongodbRepo(IArtistImageRepo):
        
    async def create(
        self,
        image: ArtistImageModel,
    ) -> ArtistImageModel:
        
        new_artist = await ArtistImageCollection(
            **image.model_dump(exclude={"id", "_id"}),
        ).insert()
        return ArtistImageModel.model_validate(new_artist, from_attributes=True)
        
    async def get_by_id(
        self,
        image_id: str,
    ) ->  ArtistImageModel:
        
        try:
                                    
            image_id = convert_object_id(image_id)
            
            image = await ArtistImageCollection.find_one(
                ArtistImageCollection.id == image_id,
            )
                        
            return ArtistImageModel.model_validate(image, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="Artist not found")

    async def update(
        self,
        image: ArtistImageModel,
    ) ->  ArtistImageModel:
        
        try:               
            
            to_update: dict = image.custom_model_dump(
                exclude_none=True,
                db_stack="no-sql",
            )
            
            await ArtistImageCollection.find(
                ArtistImageCollection.id == image.id,
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
            result = await ArtistImageCollection.find(
                ArtistImageCollection.id == image_id,
            ).delete()                       
            return bool(result.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="Artist not found")
        
    async def get_by_artist_id(
        self,
        artist_id: str,
    ) ->  list[ArtistImageModel]:
        
        try:
            artist_id = convert_object_id(artist_id)
            images_list = await ArtistImageCollection.find_many(
                ArtistImageCollection.artist_id == artist_id,
            ).to_list()            
            return [ ArtistImageModel.model_validate(image, from_attributes=True) for image in images_list ]
        except EntityNotFoundError:
            raise EntityNotFoundError(status_code=404, message="There are no artists")
    
    async def delete_by_artist_id(
        self,
        artist_id: str,
    ) -> bool:
        try:
            artist_id = convert_object_id(artist_id)
            result = await ArtistImageCollection.find(
                ArtistImageCollection.artist_id == artist_id
            ).delete()
            return bool(result.deleted_count) 
        except:
            raise EntityNotFoundError(status_code=404, message="Artist not found")
    
    async def delete_all(
        self,
    ) -> bool:
        try:
            result = await ArtistImageCollection.find_all().delete()
            return bool(result.deleted_count) 
        except:
            raise EntityNotFoundError(status_code=404, message="Artist not found")
