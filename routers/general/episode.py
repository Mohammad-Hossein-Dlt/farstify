import models
from access_token import optional_user_token_dependency
from fastapi import APIRouter, HTTPException, status
from db_dependency import db_dependency
from utills.check_follow import liked_episode
from actions.episode_actions import get_episode_full_info

router = APIRouter(prefix="/episode", tags=["General-Episode"])


@router.get("/fetch_single_episode", status_code=status.HTTP_201_CREATED)
async def fetch_single_episode(
        db: db_dependency,
        episode_id: int,
        access_token: optional_user_token_dependency,
):
    the_document, the_episode = db.query(
        models.Document,
        models.DocumentsEpisodes
    ).join(
        models.Document
    ).where(
        models.DocumentsEpisodes.Id == episode_id,
    ).first()

    if not the_episode or not the_document:
        raise HTTPException(404, "document or episode not found!")

    episode_info = await get_episode_full_info(db=db, episode=the_episode, document=the_document)

    if access_token.permission:
        episode_info.Followed = liked_episode(db=db, user_id=access_token.user_id, episode_id=the_episode.Id)

    return episode_info



