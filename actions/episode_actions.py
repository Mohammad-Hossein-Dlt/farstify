from actions_functions.listened import get_listened_times
from db_dependency import db_dependency
from pydantic import BaseModel
from typing import List, Dict
import models
from utills.encode_link import encode_link
from storage import Buckets
from utills.path_manager import make_path
from sqlalchemy import and_
from actions.artist_short_info_actions import get_artist_short_info, ArtistShortInfo
from actions.agent_actions import get_agent_with_roles, get_main_agent
from utills.get_duration import get_duration


class EpisodeFullInfo(BaseModel):
    Id: int | None = None
    Artist: ArtistShortInfo | None = None
    DocumentId: int | None = None
    Title: str | None = None
    ImageUrl: str | None = None
    ContentType: str | None = None
    Duration: str | None = None
    Agents: Dict[str, List] | None = []
    CreationDate: str | None = None
    # -----------------------------------
    Followed: bool = False


class EpisodeShortInfo(BaseModel):
    Id: int | None = None
    DocumentId: int | None = None
    Title: str | None = None
    ImageUrl: str | None = None
    Duration: str | None = None
    MainAgents: List | None = []
    CreationDate: str | None = None


class EpisodeSubDetailsInfo(BaseModel):
    Id: int | None = None
    DocumentId: int | None = None
    Title: str | None = None
    ImageUrl: str | None = None
    Duration: str | None = None
    MainAgents: List | None = []
    Likes: int | None = None
    ListenedTimes: int | None = None
    CreationDate: str | None = None


async def get_episode_full_info(
        db: db_dependency,
        episode: models.DocumentsEpisodes,
        document: models.Document | None = None,
        artist: models.Document | None = None
) -> EpisodeFullInfo:
    if not document:
        document = db.query(models.Document).where(models.Document.Id == episode.DocumentId).first()

    if not artist:
        artist = db.query(models.Artists).where(models.Artists.Id == document.Owner).first()

    data = EpisodeFullInfo()
    data.Id = episode.Id
    data.Artist = get_artist_short_info(artist)
    data.DocumentId = episode.DocumentId
    data.Title = episode.Title
    data.ImageUrl = encode_link(
        bucket_name=Buckets.DOCUMENT_BUCKET_NAME,
        path=make_path(document.DirectoryName, episode.Image, is_file=True)
    ) if episode.Image else encode_link(
        bucket_name=Buckets.DOCUMENT_BUCKET_NAME,
        path=make_path(document.DirectoryName, document.MainImage, is_file=True)
    )

    data.ContentType = document.ContentType
    data.CreationDate = episode.CreationDate
    data.Duration = get_duration(episode.Duration)
    get_agents = db.query(models.Agents).where(
        models.Agents.EpisodeId == episode.Id,
    ).order_by(
        models.Agents.OrderBy.is_(None),
        models.Agents.OrderBy.asc()
    ).all()

    main_agents, given_role_agents = await get_agent_with_roles(db, get_agents)

    data.Agents = {"Main_Agent": main_agents, "Agents": given_role_agents}

    return data


async def get_episode_sub_details_info(
        db: db_dependency,
        episode: models.DocumentsEpisodes,
        document: models.Document | None = None,
        artist: models.Document | None = None
) -> EpisodeSubDetailsInfo:
    if not document:
        document = db.query(models.Document).where(models.Document.Id == episode.DocumentId).first()

    if not artist:
        artist = db.query(models.Artists).where(models.Artists.Id == document.Owner).first()

    data = EpisodeSubDetailsInfo()
    data.Id = episode.Id
    data.Artist = get_artist_short_info(artist)
    data.DocumentId = episode.DocumentId
    data.Title = episode.Title
    data.ImageUrl = encode_link(
        bucket_name=Buckets.DOCUMENT_BUCKET_NAME,
        path=make_path(document.DirectoryName, episode.Image, is_file=True)
    ) if episode.Image else encode_link(
        bucket_name=Buckets.DOCUMENT_BUCKET_NAME,
        path=make_path(document.DirectoryName, document.MainImage, is_file=True)
    )

    data.ContentType = document.ContentType
    data.CreationDate = episode.CreationDate
    data.Duration = get_duration(episode.Duration)
    get_agents = db.query(models.Agents).where(
        models.Agents.EpisodeId == episode.Id,
    ).order_by(
        models.Agents.OrderBy.is_(None),
        models.Agents.OrderBy.asc()
    ).all()

    main_agents = await get_main_agent(db, get_agents)

    data.MainAgents = main_agents

    data.ListenedTimes = await get_listened_times(db=db, episode_id=episode.Id)

    data.Likes = db.query(models.UserLikes).where(
        and_(
            models.UserLikes.DocumentId == episode.DocumentId,
            models.UserLikes.EpisodeId == episode.Id,
        )
    ).count()
    # data.Likes = get_likes(documentId=episode.DocumentId, episodeId=episode.Id)

    return data


async def get_episode_short_info(
        db: db_dependency,
        episode: models.DocumentsEpisodes,
        document: models.Document | None = None,
) -> EpisodeShortInfo:
    if not document:
        document = db.query(models.Document).where(models.Document.Id == episode.DocumentId).first()

    data = EpisodeShortInfo()
    data.Id = episode.Id
    data.DocumentId = episode.DocumentId
    data.Title = episode.Title
    data.ImageUrl = encode_link(
        bucket_name=Buckets.DOCUMENT_BUCKET_NAME,
        path=make_path(document.DirectoryName, episode.Image, is_file=True)
    ) if episode.Image else encode_link(
        bucket_name=Buckets.DOCUMENT_BUCKET_NAME,
        path=make_path(document.DirectoryName, document.MainImage, is_file=True)
    )

    data.Duration = get_duration(episode.Duration)
    data.CreationDate = episode.CreationDate

    get_agents = db.query(models.Agents).where(
        models.Agents.EpisodeId == episode.Id,
    ).order_by(
        models.Agents.OrderBy.is_(None),
        models.Agents.OrderBy.asc()
    ).all()

    main_agents = await get_main_agent(db, get_agents)

    data.MainAgents = main_agents

    return data
