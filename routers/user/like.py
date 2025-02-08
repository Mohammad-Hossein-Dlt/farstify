import models
from passlib.context import CryptContext
from access_token import user_token_dependency
from db_dependency import db_dependency
from fastapi import APIRouter, status
from actions.response_model import ResponseMessage
from sqlalchemy import and_, asc, desc
from constants import OrderBy, ContentTypes
from actions.episode_actions import get_episode_short_info

router = APIRouter(prefix="/user/like", tags=["User-Like"])


@router.put("/like_action", status_code=status.HTTP_201_CREATED)
async def like_episode(
        db: db_dependency,
        access_token: user_token_dependency,
        episode_id: int,
):
    episode, document = db.query(
        models.DocumentsEpisodes,
        models.Document
    ).join(
        models.Document
    ).where(
        models.DocumentsEpisodes.Id == episode_id
    ).first()

    check = db.query(
        models.UserLikes
    ).where(
        models.UserLikes.UserId == access_token.user_id,
        models.UserLikes.DocumentId == episode.DocumentId,
        models.UserLikes.EpisodeId == episode_id,
    ).first()

    if not check:
        like = models.UserLikes(UserId=access_token.user_id, DocumentId=episode.DocumentId, EpisodeId=episode.Id)
        db.add(like)
        db.commit()
        return ResponseMessage(error=False, message="Ok. you liked this content.")
    else:
        db.delete(check)
        db.commit()
        return ResponseMessage(error=False, message="Ok. your like has been removed.")


@router.get("/fetch_likes", status_code=status.HTTP_200_OK)
async def fetch_likes(
        db: db_dependency,
        access_token: user_token_dependency,
        limit: int, page: int,
        order_by: OrderBy,
        content_types: ContentTypes,
):
    result = []

    docs = db.query(
        models.UserLikes,
        models.DocumentsEpisodes,
        models.Document
    ).select_from(models.UserLikes).join(
        models.DocumentsEpisodes,
    ).join(
        models.Document,
    ).filter(
        models.UserLikes.UserId == access_token.user_id,
        models.Document.ContentType == content_types,
    ).order_by(
        desc(models.UserLikes.Id) if order_by is OrderBy.desc else asc(models.UserLikes.Id)
    ).limit(
        limit
    ).offset(
        limit * page
    ).all()

    for _, episode, document in docs:
        result.append(await get_episode_short_info(db=db, episode=episode, document=document))

    return result
