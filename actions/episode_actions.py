from fastapi import HTTPException

from actions_functions.listened import get_listened_times
from db_dependency import db_dependency
from pydantic import BaseModel
from typing import List, Dict
import models
from utills.encode_link import encode_link
from storage import Buckets
from utills.path_manager import make_path
from actions.raw_artist_info_actions import get_raw_artist_info, RawArtistInfo
from actions.agent_actions import get_agent_with_roles, get_main_agent
from utills.get_duration import get_duration


class EpisodeFullInfo(BaseModel):
    Id: int | None = None
    DocumentId: int | None = None
    Title: str | None = None
    ImageUrl: str | None = None
    File: str | None = None
    ContentType: str | None = None
    Duration: str | None = None
    CreationDate: str | None = None
    Listened: int | None = None
    Agents: Dict[str, List] | None = []
    Artists: List[RawArtistInfo] | None = []
    # -----------------------------------
    Followed: bool = False


class EpisodeShortInfo(BaseModel):
    Id: int | None = None
    DocumentId: int | None = None
    Title: str | None = None
    ImageUrl: str | None = None
    File: str | None = None
    Duration: str | None = None
    CreationDate: str | None = None
    Listened: int | None = None
    MainAgents: List | None = []
    Artists: List[RawArtistInfo] | None = []
    # -----------------------------------
    Followed: bool = False


async def get_episode_full_info(
        db: db_dependency,
        episode: models.DocumentsEpisodes,
        document: models.Document | None = None,
) -> EpisodeFullInfo:
    if not document:

        document = db.query(
            models.Document
        ).where(
            models.Document.Id == episode.DocumentId
        ).first()

        if not document:
            raise HTTPException(404, "document not found!")

    artists = db.query(
        models.Artists
    ).join(
        models.DocumentsOwners,
        models.Artists.Id == models.DocumentsOwners.ArtistId
    ).filter(
        models.DocumentsOwners.DocumentId == document.Id
    ).order_by(
        models.DocumentsOwners.OrderBy.asc().nullslast(),
        models.DocumentsOwners.Id.asc(),
    ).all()

    data = EpisodeFullInfo()
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

    data.File = episode.File
    data.ContentType = document.ContentType
    data.CreationDate = episode.CreationDate
    data.Duration = get_duration(episode.Duration)
    data.Listened = await get_listened_times(db=db, episode_id=episode.Id)

    main_agents, agent_with_roles = await get_agent_with_roles(db=db, episode_id=episode.Id)
    data.Agents = {"Main_Agent": main_agents, "Agents": agent_with_roles}
    data.Artists = [get_raw_artist_info(artist) for artist in artists]

    return data


async def get_episode_short_info(
        db: db_dependency,
        episode: models.DocumentsEpisodes,
        document: models.Document | None = None,
) -> EpisodeShortInfo:
    if not document:

        document = db.query(
            models.Document
        ).where(
            models.Document.Id == episode.DocumentId
        ).first()

        if not document:
            raise HTTPException(404, "document not found!")

    artists = db.query(
        models.Artists
    ).join(
        models.DocumentsOwners,
        models.Artists.Id == models.DocumentsOwners.ArtistId
    ).filter(
        models.DocumentsOwners.DocumentId == document.Id
    ).order_by(
        models.DocumentsOwners.OrderBy.asc().nullslast(),
        models.DocumentsOwners.Id.asc(),
    ).all()

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

    data.File = episode.File
    data.Duration = get_duration(episode.Duration)
    data.CreationDate = episode.CreationDate
    main_agents = await get_main_agent(db=db, episode_id=episode.Id)
    data.MainAgents = main_agents
    data.Listened = await get_listened_times(db, episode_id=episode.Id)
    data.Artists = [get_raw_artist_info(artist) for artist in artists]

    return data
