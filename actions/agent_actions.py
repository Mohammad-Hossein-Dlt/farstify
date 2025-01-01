from fastapi import HTTPException
from pydantic import BaseModel
from actions.artist_short_info_actions import ArtistShortInfo, get_artist_short_info
from actions.response_model import ResponseMessage
from db_dependency import db_dependency
import models
from typing import List, Dict
from constants import AgentRolesEntities


class AgentViewMode(BaseModel):
    Agent_Id: int | None = None
    Role_Id: int | None = None
    Profile: ArtistShortInfo | None = None
    Name: str | None = None
    Is_Main: bool = False
    Order: int | None = None


async def add_new_agent(
        db: db_dependency,
        episode_id: int,
        artist_id: str | None = None,
        name: str | None = None,
        is_main: bool = False,
):
    params = [artist_id, name]
    given_params = sum(p is not None for p in params)

    if given_params > 1:
        raise HTTPException(403, "only one entity (artist_id or name) must be given")
    elif given_params == 0:
        raise HTTPException(403, "one entity (artist_id or name) must be given")

    agent = db.query(
        models.Agents,
    ).where(
        models.Agents.EpisodeId == episode_id,
        models.Agents.ArtistId == artist_id,
        models.Agents.Name == name,
    ).first()

    if agent:
        raise HTTPException(403, "agent already exists!")

    episode, document = db.query(
        models.DocumentsEpisodes,
        models.Document
    ).join(
        models.Document
    ).where(
        models.DocumentsEpisodes.Id == episode_id
    ).first()

    if not document or not episode:
        raise HTTPException(404, "document or episode not found!")

    artist = db.query(models.Artists).where(models.Artists.Id == artist_id).first()

    if given_params == 0 or (artist and artist.Id == artist_id):
        agent_artist_id = artist.Id
    elif not name and artist:
        agent_artist_id = artist.Id
    else:
        agent_artist_id = None

    agent = models.Agents()

    agent.EpisodeId = episode.Id
    agent.ArtistId = agent_artist_id
    agent.Name = name.strip() if name else None
    agent.IsMain = is_main

    db.add(agent)
    db.commit()

    return {'Agent_Id': agent.Id}


async def edit_agent(
        db: db_dependency,
        agent_id: str,
        artist_id: str | None = None,
        name: str | None = None,
        is_main: bool = None,
):
    params = [artist_id, name]
    given_params = sum(p is not None for p in params)

    if given_params > 1:
        raise HTTPException(403, "only one entity (artist_id or name) must be given")
    elif given_params == 0:
        raise HTTPException(403, "one entity (artist_id or name) must be given")

    name = name.strip() if name else None

    agent = db.query(
        models.Agents
    ).where(
        models.Agents.Id == agent_id,
    ).first()

    if not agent:
        raise HTTPException(404, "agent not found!")

    response = ResponseMessage(error=False, message=f"agent edited.")

    if agent:

        agent.IsMain = is_main if is_main is not None else agent.IsMain

        if name and agent.Name:

            old_name = agent.Name

            agent.Name = name
            response = ResponseMessage(error=False, message=f"agent '{old_name}' renamed to '{name}'.")

        elif artist_id and agent.ArtistId:

            new_artist = db.query(
                models.Artists
            ).where(
                models.Artists.Id == artist_id,
            ).first()

            if not new_artist:
                raise HTTPException(404, "new artist not found!")

            agent.ArtistId = artist_id

            response = ResponseMessage(error=False, message=f"new artist replaced the previous artist")

        elif artist_id and agent.Name:

            new_artist = db.query(
                models.Artists
            ).where(
                models.Artists.Id == artist_id,
            ).first()

            if not new_artist:
                raise HTTPException(404, "new artist not found!")

            agent.Name = None
            agent.ArtistId = new_artist.Id

        elif name and agent.ArtistId:

            agent.ArtistId = None
            agent.Name = name

        db.commit()

    return {'Agent_Id': agent.Id}


async def agent_view_model(
        db: db_dependency,
        agent: models.Agents,
        role: models.AgentRoles | None = None,
) -> AgentViewMode:

    data = AgentViewMode()
    data.Agent_Id = agent.Id

    if agent.ArtistId:

        artist = db.query(
            models.Artists
        ).where(
            models.Artists.Id == agent.ArtistId
        ).first()

        if not artist:
            raise HTTPException(404, "artist not found!")

        data.Profile = get_artist_short_info(artist)

    elif agent.Name:

        data.Name = agent.Name

    if role:
        data.Role_Id = role.Id

    data.Is_Main = agent.IsMain
    data.Order = agent.OrderBy

    return data


async def get_main_agent(
        db: db_dependency,
        episode_id: int,
):

    agents = db.query(
        models.Agents
    ).where(
        models.Agents.EpisodeId == episode_id,
    ).order_by(
        models.Agents.OrderBy.asc().nullslast(),
        models.Agents.Id.asc(),
    ).all()

    main_agents: List = []

    for agent in agents:
        new_agent = await agent_view_model(db, agent)
        if agent.IsMain:
            main_agents.append(new_agent)
    return main_agents


async def get_agent_with_roles(
        db: db_dependency,
        episode_id: int,
):
    main_agents: List = await get_main_agent(db=db, episode_id=episode_id)
    agents_with_assigned_roles: Dict[str, list] = dict()

    for role in AgentRolesEntities:

        agents = db.query(
            models.Agents,
            models.AgentRoles,
        ).join(
            models.AgentRoles,
        ).where(
            models.Agents.EpisodeId == episode_id,
            models.AgentRoles.Role == role,
        ).order_by(
            models.AgentRoles.OrderBy.asc().nullslast(),
            models.AgentRoles.Id.asc(),
        ).all()

        result = []

        for agent, agent_role in agents:
            x = await agent_view_model(db=db, agent=agent, role=agent_role)
            x.Order = agent_role.OrderBy
            result.append(x)

        agents_with_assigned_roles.update({role: result})

    return main_agents, agents_with_assigned_roles
