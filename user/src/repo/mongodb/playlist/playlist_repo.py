from src.repo.interface.playlist.Iplaylist_repo import IPlaylistRepo
from src.domain.schemas.playlist.playlist_model import PlaylistModel
from src.infra.database.mongodb.collections.playlist.playlist_collection import PlaylistCollection
from src.models.schemas.filter.base_filter_criteria import BaseFilterCriteria
from src.infra.exceptions.exceptions import EntityNotFoundError
from src.infra.utils.convert_id import convert_object_id

class PlaylistMongodbRepo(IPlaylistRepo):
                
    async def create(
        self,
        playlist: PlaylistModel,
    ) -> PlaylistModel:
        
        try:
            new_playlist = await PlaylistCollection(
                **playlist.model_dump(exclude={"id", "_id"}),
            ).insert()
            return PlaylistModel.model_validate(new_playlist, from_attributes=True)
        except:
            raise
            ...

    async def get_by_id(
        self,
        playlist_id: str,
    ) -> PlaylistModel:
        
        try:
            playlist_id = convert_object_id(playlist_id)
            playlist = await PlaylistCollection.find_one(
                PlaylistCollection.id == playlist_id,
            )
                        
            return PlaylistModel.model_validate(playlist, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="Playlist not found")

    async def update(
        self,
        playlist: PlaylistModel,
    ) -> PlaylistModel:
        
        try:               
            to_update: dict = playlist.custom_model_dump(
                exclude_none=True,
                db_stack="no-sql",
            )
            
            await PlaylistCollection.find(
                PlaylistCollection.id == playlist.id,
            ).update(
                {
                    "$set": to_update,
                },
            )
                                    
            return await self.get_by_id(playlist.id)
        except EntityNotFoundError:
            raise
        
    async def delete_by_id(
        self,
        playlist_id: str,
    ) -> bool:
        
        try:
            playlist_id = convert_object_id(playlist_id)
            result = await PlaylistCollection.find(
                PlaylistCollection.id == playlist_id,
            ).delete()                       
            return bool(result.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="Playlist not found")
        
    async def get_by_user_id(
        self,
        user_id: str,
        criteria: BaseFilterCriteria | None = None,
    ) -> list[PlaylistModel]:
        
        try:
            user_id = convert_object_id(user_id)
            query = PlaylistCollection.find_many(
                PlaylistCollection.user_id == user_id,
            )
            
            if criteria:
                query.skip(
                    criteria.page * criteria.limit
                ).limit(
                    criteria.limit
                ).sort(
                    PlaylistCollection.created_at if criteria.order == "asc" else -PlaylistCollection.created_at
                )
            
            playlists_list = await query.to_list()
            return [ PlaylistModel.model_validate(playlist, from_attributes=True) for playlist in playlists_list ]
        except EntityNotFoundError:
            raise EntityNotFoundError(status_code=404, message="There are no playlists")
    
    async def delete_by_user_id(
        self,
        user_id: str,
    ) -> bool:
        try:
            user_id = convert_object_id(user_id)
            result = await PlaylistCollection.find(
                PlaylistCollection.user_id == user_id
            ).delete()
            return bool(result.deleted_count) 
        except:
            raise EntityNotFoundError(status_code=404, message="Playlist not found")
    
    async def delete_all(
        self,
    ) -> bool:
        try:
            result = await PlaylistCollection.find_all().delete()
            return bool(result.deleted_count) 
        except:
            raise EntityNotFoundError(status_code=404, message="Playlist not found")
