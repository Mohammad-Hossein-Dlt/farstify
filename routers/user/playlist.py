import models
from access_token import user_token_dependency
from actions.playlist_actions import get_playlist_short_info
from db_dependency import db_dependency
from fastapi import HTTPException, status, APIRouter
from actions.response_model import ResponseMessage
from typing import List
from sqlalchemy import and_

from utills.parse_null import pars_null

router = APIRouter(prefix="/user/playlist", tags=["User-Playlist"])


@router.get("/fetch_all_playlists", status_code=status.HTTP_201_CREATED)
async def fetch_all_playlists(
        db: db_dependency,
        access_token: user_token_dependency,
        limit: int,
        page: int,
):
    pl = []
    play_lists = db.query(
        models.PlayList
    ).where(
        models.PlayList.OwnerUser == access_token.user_id
    ).limit(
        limit
    ).offset(
        limit * page
    ).all()

    if play_lists.__contains__(None):
        play_lists = []

    for i in play_lists:
        pl.append(await get_playlist_short_info(db=db, playlist=i))

    return pl


@router.post("/create_playlist", status_code=status.HTTP_201_CREATED)
async def create_playlist(
        db: db_dependency,
        access_token: user_token_dependency,
        playlist_id: int | None,
        title: str | None,
        description: str | None,
        public: bool | None = None,
):
    playlist_id = pars_null(playlist_id)
    description = pars_null(description)
    title = pars_null(title)
    if not playlist_id:

        if title is None or public is None:
            raise HTTPException(422, "title or public submitted incorrectly")

        playlist = models.PlayList()
        playlist.OwnerUser = access_token.user_id
        playlist.Title = title
        playlist.Description = description
        playlist.Public = public

        db.add(playlist)
        db.commit()

        return ResponseMessage(error=False, message="Playlist has been created!")
    else:
        playlist = db.query(
            models.PlayList
        ).where(
            and_(
                models.PlayList.Id == playlist_id,
                models.PlayList.OwnerUser == access_token.user_id
            )
        ).first()

        if not playlist:
            raise HTTPException(404, "playlist not found!")

        playlist.Title = title if title is not None else playlist.Title
        playlist.Description = description if description is not None else playlist.Description
        playlist.Public = public if public is not None else playlist.Public
        db.commit()

        return ResponseMessage(error=False, message="Playlist has been updated!")


@router.post("/add_to_playlist", status_code=status.HTTP_201_CREATED)
async def add_to_playlist(
        db: db_dependency,
        access_token: user_token_dependency,
        episode_id: int,
        play_list_id: int,
):
    playlist = db.query(
        models.PlayList
    ).where(
        and_(
            models.PlayList.Id == play_list_id,
            models.PlayList.OwnerUser == access_token.user_id,
        )
    ).first()

    if not playlist:
        raise HTTPException(403, "No episode exist.")

    episode_data = db.query(models.DocumentsEpisodes).where(
        models.DocumentsEpisodes.Id == episode_id
    ).first()

    if not episode_data:
        raise HTTPException(403, "No episode exist.")

    item = db.query(
        models.PlayListRepository
    ).where(
        and_(
            models.PlayListRepository.PlayListId == playlist.Id,
            models.PlayListRepository.EpisodesId == episode_id,
        )
    ).first()

    if not item:
        playlist_episode = models.PlayListRepository()
        playlist_episode.PlayListId = playlist.Id
        playlist_episode.DocumentId = episode_data.DocumentId
        playlist_episode.EpisodesId = episode_data.Id
        db.add(playlist_episode)
        db.commit()
        return ResponseMessage(error=False, message="Episode has been added to playlist!")
    else:
        db.delete(item)
        db.commit()
        return ResponseMessage(error=False, message="Episode has been deleted from playlist!")


@router.put("/reorder_playlist", status_code=status.HTTP_200_OK)
async def reorder_contributors(
        db: db_dependency,
        access_token: user_token_dependency,
        play_list_id: int,
        episodes_id: List[int],
):
    the_play_list = db.query(
        models.PlayList
    ).where(
        and_(
            models.PlayList.Id == play_list_id,
            models.PlayList.OwnerUser == access_token.user_id
        )
    ).first()
    if the_play_list:
        for i in episodes_id:
            check = db.query(
                models.PlayListRepository
            ).where(
                and_(
                    models.PlayListRepository.EpisodesId == i,
                    models.PlayListRepository.PlayListId == the_play_list.Id,
                )
            ).first()
            if check:
                check.OrderBy = episodes_id.index(i)
                db.commit()

    return ResponseMessage(error=False, message="Contributors has been reordered!")


@router.delete("/delete_playlist", status_code=status.HTTP_201_CREATED)
async def delete_playlist(
        db: db_dependency,
        access_token: user_token_dependency,
        play_list_id: int,
):
    the_play_list = db.query(
        models.PlayList
    ).where(
        and_(
            models.PlayList.Id == play_list_id,
            models.PlayList.OwnerUser == access_token.user_id,
        )
    ).first()

    if the_play_list:
        db.delete(the_play_list)
        db.commit()

    return ResponseMessage(error=False, message="Playlist has been deleted!")
