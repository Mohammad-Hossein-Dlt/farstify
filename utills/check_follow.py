from db_dependency import db_dependency
from models import UserFollowing, UserLikes
from sqlalchemy import and_


async def artist_follow(
        db: db_dependency,
        user_id: int,
        artist_id: int,
) -> bool:
    follow = db.query(UserFollowing).where(
        and_(
            UserFollowing.UserId == user_id,
            UserFollowing.ArtistId == artist_id,
        )
    ).first()
    return True if follow else False


async def document_follow(
        db: db_dependency,
        user_id: int,
        document_id: int,
) -> bool:
    follow = db.query(UserFollowing).where(
        and_(
            UserFollowing.UserId == user_id,
            UserFollowing.DocumentId == document_id,
        )
    ).first()
    return True if follow else False


async def playlist_follow(
        db: db_dependency,
        user_id: int,
        playlist_id: int,
) -> bool:
    follow = db.query(UserFollowing).where(
        and_(
            UserFollowing.UserId == user_id,
            UserFollowing.PlayListId == playlist_id,
        )
    ).first()
    return True if follow else False


async def liked_episode(
        db: db_dependency,
        user_id: int,
        episode_id: int,
) -> bool:
    like = db.query(UserLikes).where(
        and_(
            UserLikes.UserId == user_id,
            UserLikes.EpisodeId == episode_id,
        )
    ).first()
    return True if like else False

