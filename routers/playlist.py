import models
from fastapi import APIRouter, status, HTTPException
from db_dependency import db_dependency
from actions.episode_actions import get_episode_short_info
from actions.playlist_actions import get_playlist_full_info
from access_token import optional_user_token_dependency
from utills.check_follow import playlist_follow
from constants import OrderBy

router = APIRouter(prefix="/playlist", tags=["PlayList"])


@router.get("/fetch_playlist", status_code=status.HTTP_201_CREATED)
async def fetch_playlist(
        db: db_dependency,
        play_list_id: int,
        access_token: optional_user_token_dependency,
):
    play_list = db.query(models.PlayList).where(
        models.PlayList.Id == play_list_id,
    ).first()

    if not play_list:
        raise HTTPException(404, "playlist not found!")

    play_list_info = await get_playlist_full_info(db=db, playlist=play_list)
    if access_token.permission:
        play_list_info.Followed = playlist_follow(db=db, user_id=access_token.user_id, playlist_id=play_list_info.Id)
    return play_list_info


@router.get("/fetch_playlist_episodes", status_code=status.HTTP_201_CREATED)
async def fetch_playlist_episodes(
        db: db_dependency,
        play_list_id: int,
        order_by: OrderBy,
):
    result = []

    episodes = db.query(
        models.PlayListRepository,
        models.DocumentsEpisodes,
        models.Document
    ).join(
        models.DocumentsEpisodes,
        models.PlayListRepository.EpisodesId == models.DocumentsEpisodes.Id,
        isouter=True
    ).join(
        models.Document,
        models.PlayListRepository.DocumentId == models.Document.Id,
        isouter=True
    ).where(
        models.PlayListRepository.PlayListId == play_list_id,
    ).order_by(
        (
            models.Agents.OrderBy.is_(None),
            models.Agents.OrderBy.asc()
        ) if order_by == OrderBy.asc else
        (
            models.Agents.OrderBy.is_not(None),
            models.Agents.OrderBy.desc()
        )
    ).all()

    for _, episode, document in episodes:
        result.append(await get_episode_short_info(db=db, episode=episode, document=document))

    return result
