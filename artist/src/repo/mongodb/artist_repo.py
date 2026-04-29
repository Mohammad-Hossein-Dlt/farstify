from src.repo.interface.Iartist_repo import IArtistRepo
from src.domain.schemas.artist.artist_model import ArtistModel
from src.infra.database.mongodb.collections.artist_collection import ArtistCollection
from src.infra.exceptions.exceptions import EntityNotFoundError, DuplicateEntityError
from src.infra.utils.convert_id import convert_object_id

class ArtistMongodbRepo(IArtistRepo):
        
    async def create_artist(
        self,
        artist: ArtistModel,
    ) -> ArtistModel:
        
        try:
            await self.get_artist_by_name(artist.name)
            raise DuplicateEntityError(409, "Artist already exist")
        except EntityNotFoundError:
            new_artist = await ArtistCollection(
                **artist.model_dump(exclude={"id", "_id"}),
            ).insert()
            return ArtistModel.model_validate(new_artist, from_attributes=True)
    
    async def get_artist_by_name(
        self,
        name: str,
    ) -> ArtistModel:
        
        try:
            result = await ArtistCollection.find_one(
                ArtistCollection.name == name,
            )
            return ArtistModel.model_validate(result, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="Artist not found")
        
    async def get_artist_by_id(
        self,
        artist_id: str,
    ) ->  ArtistModel:
        
        try:
                                    
            artist_id = convert_object_id(artist_id)
            
            artist = await ArtistCollection.find_one(
                ArtistCollection.id == artist_id,
            )
                        
            return ArtistModel.model_validate(artist, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="Artist not found")

    async def update_artist(
        self,
        artist: ArtistModel,
    ) ->  ArtistModel:
        
        try:               
            
            to_update: dict = artist.custom_model_dump(
                # exclude_unset=True,
                exclude_none=True,
                db_stack="no-sql",
            )
            
            await ArtistCollection.find(
                ArtistCollection.id == artist.id,
            ).update(
                {
                    "$set": to_update,
                },
            )
                        
            return await self.get_artist_by_id(artist.id)
        except EntityNotFoundError:
            raise
        
    async def delete_artist(
        self,
        artist_id: str,
    ) -> bool:
        
        try:
            artist_id = convert_object_id(artist_id)
            delete_artist = await ArtistCollection.find(
                ArtistCollection.id == artist_id,
            ).delete()                       
            return bool(delete_artist.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="Artist not found")
    
    async def get_all_artists(
        self,
    ) -> list[ArtistModel]:    
        try:
            artists_list = await ArtistCollection.find_all().to_list()            
            return [ ArtistModel.model_validate(artist, from_attributes=True) for artist in artists_list ]
        except:
            raise EntityNotFoundError(status_code=404, message="Artist not found")
    
    async def delete_all_artists(
        self,
    ) -> bool:
        try:
            delete_artists = await ArtistCollection.delete_all()
            return bool(delete_artists.deleted_count) 
        except:
            raise EntityNotFoundError(status_code=404, message="Artist not found")
