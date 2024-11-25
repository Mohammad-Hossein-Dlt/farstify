import models
from access_token import artist_token_dependency
from db_dependency import db_dependency
from fastapi import APIRouter, HTTPException, status
from actions.response_model import ResponseMessage
from actions.agent_actions import get_agent_with_roles
from typing import List
from sqlalchemy import and_
from constants import AgentRolesEntities
from utills.exceptions import owned_exception
from utills.check_ownership import is_episode_owned_by_artist

router = APIRouter(prefix="/agents", tags=["Agents"])


@router.post("/add_agent", status_code=status.HTTP_200_OK)
async def add_agent(
        db: db_dependency,
        artist_id: int,
        episode_id: int,
        agent_id: str | None = None,
        name: str | None = None,
        is_main: bool = False,
):
    params = [agent_id, name]
    given_params = sum(p is not None for p in params)

    if given_params > 1:
        raise HTTPException(403, "only one entity must be given")

    episode, document = db.query(models.DocumentsEpisodes, models.Document).join(
        models.Document
    ).where(
        models.DocumentsEpisodes.Id == episode_id
    ).first()

    if not await is_episode_owned_by_artist(db, episode_id=episode.Id, artist_id=artist_id):
        raise owned_exception

    agent_artist = db.query(models.Artists).where(models.Artists.Id == agent_id).first()

    if agent_id and not agent_artist:
        raise HTTPException(403, f"artist {agent_id} not exist.")

    agent_artist_id = None

    if given_params == 0 or (agent_artist and agent_artist.Id == artist_id):
        agent_artist_id = artist_id
    elif not name and agent_artist:
        agent_artist_id = agent_artist.Id
    else:
        agent_artist_id = None

    agent = models.Agents()

    agent.OwnerId = artist_id
    agent.EpisodeId = episode.Id
    agent.ArtistId = agent_artist_id
    agent.Name = name.strip() if name else None
    agent.IsMain = is_main

    db.add(agent)
    db.commit()

    return ResponseMessage(error=False, message="New agent has been added.")


@router.post("/add_agent_role", status_code=status.HTTP_200_OK)
async def add_agent(
        db: db_dependency,
        artist_id: int,
        agent_id: int,
        role: AgentRolesEntities,
):
    agent = db.query(models.Agents).where(models.Agents.Id == agent_id).first()
    if agent and agent.OwnerId == artist_id:
        new_role = models.AgentRoles()
        new_role.AgentId = agent.Id
        new_role.Role = role
        db.add(new_role)
        db.commit()


@router.get("/fetch_agents", status_code=status.HTTP_200_OK)
async def fetch_agent(
        db: db_dependency,
        artist_id: int,
        episode_id: int,
):
    if not await is_episode_owned_by_artist(db, artist_id=artist_id, episode_id=episode_id):
        raise owned_exception

    get_agents = db.query(models.Agents).where(
        models.Agents.EpisodeId == episode_id,
    ).order_by(
        models.Agents.OrderBy.is_(None),
        models.Agents.OrderBy.asc()
    ).all()

    main_agents, given_role_agents = await get_agent_with_roles(db, get_agents)

    return {"Main_Agent": main_agents, "Agents": given_role_agents}


@router.put("/edit_agent", status_code=status.HTTP_200_OK)
async def remove_agent(
        db: db_dependency,
        artist_id: int,
        agent_id: int,
        name: str | None = None,
        is_main: bool = None,
):
    name = name.strip() if name else None

    agent = db.query(models.Agents).where(
        and_(
            models.Agents.Id == agent_id,
            models.Agents.OwnerId == artist_id,
        )
    ).first()

    response = ResponseMessage(error=False, message=f"Ok. agent has been edited")

    if agent:
        old_name = agent.Name
        agent.IsMain = is_main if is_main is not None else agent.IsMain
        if name and agent.Name and agent.Name != name and not agent.ArtistId:
            agent.Name = name
            response = ResponseMessage(error=False, message=f"agent '{old_name}' has been renamed to '{name}'.")
        elif agent.ArtistId:
            response = ResponseMessage(error=False, message=f"agent '{name}' is an artist.")

        db.commit()

    return response


@router.put("/reorder_agent", status_code=status.HTTP_200_OK)
async def reorder_agent(
        db: db_dependency,
        artist_id: int,
        episode_id: int,
        agents_ids: List[int],
):
    get_agents = db.query(models.Agents).where(
        and_(
            models.Agents.OwnerId == artist_id,
            models.Agents.EpisodeId == episode_id,
        )
    ).all()

    for index, agent_id in enumerate(agents_ids):
        for agent in get_agents:
            if agent.Id == agent_id:
                agent.OrderBy = index

    db.commit()

    return ResponseMessage(error=False, message=f" agents has been reordered.")


@router.put("/reorder_roles", status_code=status.HTTP_200_OK)
async def reorder_agent(
        db: db_dependency,
        artist_id: int,
        episode_id: int,
        role: AgentRolesEntities,
        agents_roles_ids: List[int],
):
    get_agents_roles = db.query(models.AgentRoles).join(models.Agents).where(
        and_(
            models.Agents.OwnerId == artist_id,
            models.Agents.EpisodeId == episode_id,
            models.AgentRoles.Role == role,
        )
    ).all()

    for index, agent_role_id in enumerate(agents_roles_ids):
        for agent_role in get_agents_roles:
            if agent_role.AgentId == agent_role_id:
                agent_role.OrderBy = index

    db.commit()

    return ResponseMessage(error=False, message=f"{role}'s agents has been reordered.")


@router.delete("/remove_agent", status_code=status.HTTP_200_OK)
async def remove_agent(
        db: db_dependency,
        artist_id: int,
        agent_id: int,
):
    try:
        agent = db.query(models.Agents).where(
            and_(
                models.Agents.Id == agent_id,
                models.Agents.OwnerId == artist_id,
            )
        ).first()

        if agent:
            db.delete(agent)
            db.commit()

        return ResponseMessage(error=False, message=f"agent has been removed.")

    except Exception as ex:
        return ResponseMessage()


@router.delete("/remove_agent_role", status_code=status.HTTP_200_OK)
async def remove_agent_role(
        db: db_dependency,
        artist_id: int,
        role_id: int,
):
    try:
        role, agent = db.query(models.AgentRoles, models.Agents).join(
            models.Agents
        ).where(
            and_(
                models.AgentRoles.Id == role_id,
                models.Agents.OwnerId == artist_id,
            )
        ).first()

        if role and agent:
            db.delete(role)
            db.commit()

        return ResponseMessage(error=False, message=f"agent role has been removed.")

    except Exception as ex:
        return ResponseMessage()
