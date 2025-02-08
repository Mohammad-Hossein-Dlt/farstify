import models
from enum import Enum
from sqlalchemy import and_, func, desc, asc
from actions_functions.listened import get_listened_times
from db_dependency import db_dependency
from pydantic import BaseModel
from typing import List
from utills.path_manager import make_path
from utills.encode_link import encode_link
from storage import Buckets
from constants import OrderBy
from actions.document_actions import get_document_short_info
from actions.episode_actions import get_episode_short_info
from actions.link_actions import LinkData, get_link_data


class ArtistPageInfo(BaseModel):
    Id: int | None = None
    Name: str | None = None
    ProfileImageUrl: str | None = None
    ContentType: str | None = None
    Following: int | None = None
    ListenedTimes: int | None = None
    Published: int | None = None
    Links: List[LinkData] = []
    # -----------------------------------
    Followed: bool = False


class ArtistProfileInfo(BaseModel):
    Id: int | None = None
    Name: str | None = None
    ProfileImageUrl: str | None = None
    ImagesUrls: List[str] = []
    ContentType: str | None = None
    Following: int | None = None
    ListenedTimes: int | None = None
    Published: int | None = None
    Links: List[LinkData] = []
    # -----------------------------------
    Followed: bool = False


class ArtistDocumentsSortBy(str, Enum):
    all_base_on_date = "all_base_on_date"
    all_base_on_popularity = "all_base_on_popularity"
    owned = "owned"
    contributed = "contributed"


async def get_artist_page_info(
        db: db_dependency,
        artist: models.Artists
) -> ArtistPageInfo:
    data = ArtistPageInfo()

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

    data.Published = db.query(
        models.Document
    ).join(
        models.DocumentsOwners,
        models.Document.Id == models.DocumentsOwners.DocumentId
    ).filter(
        and_(
            models.DocumentsOwners.ArtistId == artist.Id,
            models.Document.Active.is_(True),
        )
    ).count()

    links = db.query(
        models.ArtistLinks
    ).where(
        models.ArtistLinks.ArtistId == artist.Id,
    ).order_by(
        asc(models.ArtistLinks.OrderBy).nullslast(),
        asc(models.ArtistLinks.Id),
    ).all()

    data.Links = [get_link_data(link) for link in links]

    return data


async def get_artist_profile_info(
        db: db_dependency,
        artist: models.Artists
) -> ArtistProfileInfo:
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

    data.Published = db.query(
        models.Document
    ).join(
        models.DocumentsOwners,
        models.Document.Id == models.DocumentsOwners.DocumentId
    ).filter(
        and_(
            models.DocumentsOwners.ArtistId == artist.Id,
            models.Document.Active.is_(True),
        )
    ).count()

    links = db.query(
        models.ArtistLinks
    ).where(
        models.ArtistLinks.ArtistId == artist.Id,
    ).order_by(
        asc(models.ArtistLinks.OrderBy).nullslast(),
        asc(models.ArtistLinks.Id),
    ).all()

    data.Links = [get_link_data(link) for link in links]

    images = db.query(models.ArtistImages).where(
        models.ArtistImages.ArtistId == artist.Id
    ).order_by(
        asc(models.ArtistImages.OrderBy).nullslast(),
        asc(models.ArtistImages.Id),
    ).all()

    for image in images:
        data.ImagesUrls.append(
            encode_link(
                bucket_name=Buckets.USER_BUCKET_NAME,
                path=make_path(artist.DirectoryName, image.Image, is_file=True)
            )
        )
    return data


async def get_best_documents(
        db: db_dependency,
        artist_id: int,
        limit: int,
        page: int,
):
    # sub = db.query(
    #     models.Document, func.max(models.ListenedHistory.DocumentId).label("max_listened")
    # ).outerjoin(
    #     models.ListenedHistory
    # ).group_by(
    #     models.Document.Id
    # ).subquery()
    #
    # docs = db.query(
    #     models.Document
    # ).join(
    #     sub,
    #     models.Document.Id == sub.c.Id
    # ).join(
    #     models.DocumentsOwners,
    #     models.Document.Id == models.DocumentsOwners.DocumentId
    # ).where(
    #     models.DocumentsOwners.ArtistId == admin.Id
    # ).order_by(
    #     desc(sub.c.max_listened)
    # ).limit(
    #     limit
    # ).offset(
    #     limit * page
    # ).all()

    docs = db.query(
        models.Document
    ).join(
        models.DocumentsOwners,
        models.Document.Id == models.DocumentsOwners.DocumentId
    ).where(
        models.DocumentsOwners.ArtistId == artist_id,
    ).order_by(
        desc(models.Document.Id),
    ).limit(
        limit
    ).offset(
        limit * page
    ).all()

    return [await get_document_short_info(db, i) for i in docs]


async def get_best_episodes(
        db: db_dependency,
        artist_id: int,
        limit: int,
        page: int,
):
    sub = db.query(
        models.DocumentsEpisodes,
        func.max(models.ListenedHistory.Id).label("max_listened")
    ).outerjoin(
        models.ListenedHistory
    ).group_by(
        models.DocumentsEpisodes.Id
    ).subquery()

    episodes = db.query(
        models.DocumentsEpisodes
    ).join(
        sub,
        models.DocumentsEpisodes.Id == sub.c.Id
    ).join(
        models.Agents,
        models.DocumentsEpisodes.Id == models.Agents.EpisodeId,
    ).where(
        models.Agents.ArtistId == artist_id,
        models.Agents.IsMain.is_(True),
    ).order_by(
        desc(sub.c.max_listened)
    ).limit(
        limit
    ).offset(
        limit * page
    ).all()

    return [await get_episode_short_info(db, i) for i in episodes]


async def get_all_artist_documents(
        db: db_dependency,
        artist_id: int,
        sort: ArtistDocumentsSortBy,
        limit: int,
        page: int,
        order_by: OrderBy,
):
    result = []
    docs = []

    if sort == ArtistDocumentsSortBy.contributed:

        subquery = db.query(
            models.DocumentsOwners.DocumentId,
            func.count(models.DocumentsOwners.ArtistId).label('artist_count')
        ).group_by(
            models.DocumentsOwners.DocumentId
        ).subquery()

        docs = db.query(
            models.Document
        ).join(
            models.DocumentsOwners,
            models.Document.Id == models.DocumentsOwners.DocumentId
        ).join(
            subquery,
            models.Document.Id == subquery.c.DocumentId
        ).filter(
            and_(
                models.DocumentsOwners.ArtistId == artist_id,
                subquery.c.artist_count > 1
            )
        ).order_by(
            desc(models.Document.Id) if order_by is OrderBy.desc else asc(models.Document.Id)
        ).limit(
            limit
        ).offset(
            limit * page
        ).all()

    elif sort == ArtistDocumentsSortBy.owned:

        subquery = db.query(
            models.DocumentsOwners.DocumentId,
            func.count(models.DocumentsOwners.ArtistId).label('artist_count')
        ).group_by(
            models.DocumentsOwners.DocumentId
        ).subquery()

        docs = db.query(
            models.Document
        ).join(
            models.DocumentsOwners,
            models.Document.Id == models.DocumentsOwners.DocumentId
        ).join(
            subquery,
            models.Document.Id == subquery.c.DocumentId
        ).filter(
            and_(
                models.DocumentsOwners.ArtistId == artist_id,
                subquery.c.artist_count == 1
            )
        ).order_by(
            desc(models.Document.Id) if order_by is OrderBy.desc else asc(models.Document.Id)
        ).limit(
            limit
        ).offset(
            limit * page
        ).all()

    elif sort == ArtistDocumentsSortBy.all_base_on_popularity:

        sub = db.query(
            models.DocumentsEpisodes.DocumentId,
            func.count(models.ListenedHistory.Id).label("max_listened")
        ).outerjoin(
            models.ListenedHistory,
            models.ListenedHistory.EpisodeId == models.DocumentsEpisodes.Id
        ).group_by(
            models.DocumentsEpisodes.Id
        ).subquery()

        docs = db.query(
            models.Document,
        ).outerjoin(
            sub,
            sub.c.DocumentId == models.Document.Id,
        ).join(
            models.DocumentsOwners,
            models.DocumentsOwners.DocumentId == models.Document.Id,
        ).where(
            models.DocumentsOwners.ArtistId == artist_id,
        ).order_by(
            desc(sub.c.max_listened).nullslast() if order_by is OrderBy.desc else asc(sub.c.max_listened).nullsfirst()
        ).limit(
            limit
        ).offset(
            limit * page
        ).all()

    else:
        docs = db.query(
            models.Document
        ).join(
            models.DocumentsOwners,
            models.Document.Id == models.DocumentsOwners.DocumentId
        ).filter(
            models.DocumentsOwners.ArtistId == artist_id,
        ).order_by(
            desc(models.Document.Id) if order_by is OrderBy.desc else asc(models.Document.Id)
        ).limit(
            limit
        ).offset(
            limit * page
        ).all()

    for i in docs:
        result.append(await get_document_short_info(db=db, document=i))

    return result


async def get_artist_appears_on_documents(
        db: db_dependency,
        artist_id: int,
        limit: int,
        page: int,
        order_by: OrderBy,
):
    result = []

    agents = db.query(
        models.Agents.EpisodeId,
    ).filter(
        models.Agents.ArtistId == artist_id,
    ).subquery()

    owners = db.query(
        models.DocumentsOwners.DocumentId,
    ).filter(
        models.DocumentsOwners.ArtistId == artist_id,
    ).subquery()

    docs = db.query(
        models.Document,
    ).join(
        models.DocumentsEpisodes
    ).filter(
        models.DocumentsEpisodes.Id.in_(agents),
        models.Document.Id.notin_(owners)
    ).order_by(
        desc(models.Document.Id) if order_by is OrderBy.desc else asc(models.Document.Id)
    ).limit(
        limit
    ).offset(
        limit * page
    ).all()

    for i in docs:
        result.append(await get_document_short_info(db=db, document=i))

    return result


async def get_artist_appears_on_episodes(
        db: db_dependency,
        artist_id: int,
        limit: int,
        page: int,
        order_by: OrderBy,
):
    result = []

    agents = db.query(
        models.Agents.EpisodeId,
    ).filter(
        models.Agents.ArtistId == artist_id,
    ).subquery()

    owners = db.query(
        models.DocumentsOwners.DocumentId,
    ).filter(
        models.DocumentsOwners.ArtistId == artist_id,
    ).subquery()

    contribution = db.query(
        models.Document,
        models.DocumentsEpisodes,
    ).join(
        models.Document
    ).filter(
        models.DocumentsEpisodes.Id.in_(agents),
        models.Document.Id.not_in(owners)
    ).order_by(
        desc(models.DocumentsEpisodes.Id) if order_by is OrderBy.desc else asc(models.DocumentsEpisodes.Id)
    ).limit(
        limit
    ).offset(
        limit * page
    ).all()

    for document, episode in contribution:
        result.append(await get_episode_short_info(db=db, episode=episode, document=document))

    return result
