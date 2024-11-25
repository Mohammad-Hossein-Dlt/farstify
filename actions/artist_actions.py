import models
from enum import Enum
from sqlalchemy import and_, func, desc

from actions_functions.listened import get_listened_times
from db_dependency import db_dependency
from pydantic import BaseModel
from typing import List
from sqlalchemy import or_
from utills.path_manager import make_path
from utills.encode_link import encode_link
from storage import Buckets
from constants import ContentTypes, OrderBy
from actions.document_actions import get_document_short_info
from actions.episode_actions import get_episode_short_info
from actions.link_actions import LinkData


class ArtistPersonalInfo(BaseModel):
    Id: int | None = None
    Name: str | None = None
    ProfileImageUrl: str | None = None
    ImagesUrls: List[str] = []
    ContentType: str | None = None
    Following: int | None = None
    ListenedTimes: int | None = None
    Published: int | None = None
    Links: List[LinkData] = []
    Followed: bool = False


class ArtistProfileInfo(BaseModel):
    Id: int | None = None
    Name: str | None = None
    ProfileImageUrl: str | None = None
    ContentType: str | None = None
    Following: int | None = None
    ListenedTimes: int | None = None
    # -----------------------------------
    Followed: bool = False


class ArtistDocumentOrder(str, Enum):
    all = "all"
    owned = "owned"
    contributed = "contributed"


async def get_artist_profile_info(
        db: db_dependency,
        artist: models.Artists
) -> ArtistProfileInfo and int:
    data = ArtistProfileInfo()

    data.Id = artist.Id

    data.Name = artist.Name

    data.ProfileImageUrl = encode_link(
        bucket_name=Buckets.USER_BUCKET_NAME,
        path=make_path(artist.DirectoryName, artist.ProfileImage, is_file=True)
    ) if artist.ProfileImage else None

    data.ContentType = artist.ContentType

    data.Following = db.query(models.UserFollowing).where(
        and_(
            models.UserFollowing.ArtistId == artist.Id,
        )
    ).count()

    data.ListenedTimes = await get_listened_times(db=db, artist_id=artist.Id)

    return data, artist.Id


async def get_artist_personal_info(
        db: db_dependency,
        artist: models.Artists
) -> ArtistPersonalInfo:
    data = ArtistPersonalInfo()

    data.Id = artist.Id

    data.Name = artist.Name

    data.ProfileImageUrl = encode_link(
        bucket_name=Buckets.USER_BUCKET_NAME,
        path=make_path(artist.DirectoryName, artist.ProfileImage, is_file=True)
    ) if artist.ProfileImage else None

    data.ContentType = artist.ContentType

    data.Following = db.query(models.UserFollowing).where(
        and_(
            models.UserFollowing.ArtistId == artist.Id,
        )
    ).count()

    data.ListenedTimes = await get_listened_times(db=db, artist_id=artist.Id)

    data.Published = db.query(models.Document).where(
        and_(
            models.Document.Owner == artist.Id,
            models.Document.Active == True,
        )
    ).count()

    links = db.query(models.ArtistLinks).where(
        models.ArtistLinks.ArtistId == artist.Id,
    ).order_by(
        models.ArtistLinks.OrderBy.is_(None),
        models.ArtistLinks.OrderBy.asc()
    ).all()

    data.Links = [LinkData(Title=l.Title, Link=l.Link) for l in links]

    images = db.query(models.ArtistImages).where(
        models.ArtistImages.ArtistId == artist.Id
    ).order_by(
        models.ArtistImages.OrderBy.is_(None),
        models.ArtistImages.OrderBy.asc()
    ).all()

    for img in images:
        data.ImagesUrls.append(encode_link(
            bucket_name=Buckets.USER_BUCKET_NAME,
            path=make_path(artist.DirectoryName, img.Image, is_file=True)
        )
        )
    return data


async def fetch_profile(db: db_dependency, artist_id: int) -> ArtistProfileInfo:
    user = db.query(models.Artists).where(models.Artists.Id == artist_id).first()
    if not user:
        return ArtistProfileInfo()

    return await get_artist_profile_info(db, user)


async def best_documents(
        db: db_dependency,
        artist_id: int,
        limit: int,
        page: int,
):

    artist = db.query(models.Artists).where(models.Artists.Id == artist_id).first()

    sub = db.query(
        models.Document, func.max(models.ListenedHistory.DocumentId).label("max_listened")
    ).outerjoin(
        models.ListenedHistory
    ).group_by(
        models.Document.Id
    ).subquery()

    docs = db.query(models.Document).join(
        sub,
        models.Document.Id == sub.c.Id
    ).where(
        models.Document.Owner == artist.Id
    ).order_by(
        desc(sub.c.max_listened)
    ).limit(limit).offset(limit * page).all()

    return [await get_document_short_info(db, i, artist) for i in docs]


async def best_episodes(
        db: db_dependency,
        artist_id: int,
        limit: int,
        page: int,
):
    artist = db.query(models.Artists).where(models.Artists.Id == artist_id).first()

    sub = db.query(
        models.DocumentsEpisodes, func.max(models.ListenedHistory.DocumentId).label("max_listened")
    ).outerjoin(
        models.ListenedHistory
    ).group_by(
        models.DocumentsEpisodes.Id
    ).subquery()

    episodes = db.query(models.DocumentsEpisodes).join(
        sub,
        models.DocumentsEpisodes.Id == sub.c.Id
    ).join(
        models.Document,
        models.Document.Owner == artist.Id,
    ).order_by(
        desc(sub.c.max_listened)
    ).limit(limit).offset(limit * page).all()

    return [await get_episode_short_info(db, i) for i in episodes]


async def fetch_all_artist_documents(
        db: db_dependency,
        artist_id: int,
        sort: ArtistDocumentOrder,
        singles: bool,
        limit: int,
        page: int,
        order_by: OrderBy,
        from_type: ContentTypes | None = None,
):
    result = []
    artist = db.query(models.Artists).where(models.Artists.Id == artist_id).first()

    if not artist:
        return []

    content_type = artist.ContentType if not from_type else from_type.value

    if sort == ArtistDocumentOrder.owned:

        docs = db.query(models.Document).filter(
            and_(
                models.Document.ContentType == content_type,
                models.Document.Single == False if not singles else models.Document.Single == True,
                models.Document.Owner == artist.Id,
            ),
        ).order_by(
            models.Document.Id.desc() if order_by is OrderBy.desc else models.Document.Id.asc()
        ).limit(limit).offset(limit * page).all()

    elif sort == ArtistDocumentOrder.contributed:

        docs = db.query(models.Document).distinct().filter(
            and_(
                models.Document.ContentType == content_type,
                models.Document.Single == False if not singles else models.Document.Single == True,
                models.Document.contributors.any(ArtistId=artist.Id),
            ),
        ).order_by(
            models.Document.Id.desc() if order_by is OrderBy.desc else models.Document.Id.asc()
        ).limit(limit).offset(limit * page).all()

    else:

        docs = db.query(models.Document).distinct().filter(
            and_(
                models.Document.ContentType == content_type,
                models.Document.Single == False if not singles else models.Document.Single == True,
                or_(
                    models.Document.Owner == artist.Id,
                    models.Document.contributors.any(ArtistId=artist.Id),
                ),
            ),
        ).order_by(
            models.Document.Id.desc() if order_by is OrderBy.desc else models.Document.Id.asc()
        ).limit(limit).offset(limit * page).all()

    if not docs or docs.__contains__(None):
        return []

    for i in docs:
        result.append(await get_document_short_info(db=db, document=i, artist=artist))

    return result


async def fetch_artist_appears_on_documents(
        db: db_dependency,
        artist_id: int,
        limit: int,
        page: int,
        order_by: OrderBy,
):
    result = []
    artist = db.query(models.Artists).where(models.Artists.Id == artist_id).first()

    if not artist:
        return []

    docs = db.query(models.Document).select_from(
        models.Contributors,
    ).where(
        models.Contributors.ArtistId == artist.Id,
    ).order_by(
        models.Document.Id.desc() if order_by is OrderBy.desc else models.Document.Id.asc()
    ).limit(limit).offset(limit * page).all()

    if not docs or docs.__contains__(None):
        return []

    for i in docs:
        result.append(await get_document_short_info(db=db, document=i, artist=artist))

    return result


async def fetch_artist_appears_on_episodes(
        db: db_dependency,
        artist_id: int,
        limit: int,
        page: int,
        order_by: OrderBy,
):
    result = []
    artist = db.query(models.Artists).where(models.Artists.Id == artist_id).first()

    if not artist:
        return []

    contribution = db.query(models.Document, models.DocumentsEpisodes).select_from(models.Agents).where(
        models.Agents.ArtistId == artist.Id,
    ).order_by(
        models.Agents.Id.desc() if order_by is OrderBy.desc else models.Agents.Id.asc()
    ).limit(limit).offset(limit * page).all()

    if not contribution or contribution.__contains__(None):
        return []

    for document, episode in contribution:
        result.append(await get_episode_short_info(db=db, episode=episode, document=document))

    return result
