import models
from db_dependency import db_dependency
from fastapi import APIRouter, HTTPException, status
from actions.response_model import ResponseMessage
from actions.agent_actions import add_new_agent, get_agent_with_roles, agent_view_model, edit_agent
from typing import List
from sqlalchemy import and_
from constants import AgentRolesEntities
from utills.parse_null import pars_null

router = APIRouter(prefix="/admin/agents", tags=["Admin-Agents"])


@router.post("/insert_agent", status_code=status.HTTP_200_OK)
async def insert_agent(
        db: db_dependency,
        episode_id: int,
        agent_id: int | str | None = None,  # none or null in str can be given, then with pars_null function it is converted to None
        artist_id: int | str | None = None, # none or null in str can be given, then with pars_null function it is converted to None
        name: str | None = None,
        is_main: bool = False,
):
    agent_id = pars_null(agent_id)
    artist_id = pars_null(artist_id)
    name = pars_null(name)

    print(agent_id)

    if agent_id and int(agent_id):
        return await edit_agent(
            db=db,
            agent_id=agent_id,
            artist_id=artist_id,
            name=name,
            is_main=is_main,
        )

    else:
        return await add_new_agent(
            db=db,
            episode_id=episode_id,
            artist_id=artist_id,
            name=name,
            is_main=is_main
        )


@router.post("/insert_agent_role", status_code=status.HTTP_200_OK)
async def insert_agent(
        db: db_dependency,
        agent_id: int,
        role: AgentRolesEntities,
):
    agent = db.query(
        models.Agents
    ).where(
        models.Agents.Id == agent_id
    ).first()

    if not agent:
        raise HTTPException(404, "agent not found!")

    new_role = db.query(
        models.AgentRoles,
    ).where(
        models.AgentRoles.AgentId == agent.Id,
        models.AgentRoles.Role == role.name,
    ).first()

    if new_role:
        raise HTTPException(403, "agent role already exists!")

    new_role = models.AgentRoles()
    new_role.AgentId = agent.Id
    new_role.Role = role
    db.add(new_role)
    db.commit()

    return ResponseMessage(
        Error=False,
        Content={
            'Message': 'new agent role added',
            'Role_Id': new_role.Id,
        },
    )


@router.get("/fetch_single_agent", status_code=status.HTTP_200_OK)
async def fetch_agent(
        db: db_dependency,
        agent_id: int,
):
    agent = db.query(
        models.Agents
    ).where(
        models.Agents.Id == agent_id,
    ).first()

    if not agent:
        raise HTTPException(404, "agent not found!")

    return await agent_view_model(db, agent)


@router.get("/fetch_raw_agents", status_code=status.HTTP_200_OK)
async def fetch_agent(
        db: db_dependency,
        episode_id: int,
):
    results = []

    agents = db.query(
        models.Agents
    ).where(
        models.Agents.EpisodeId == episode_id,
    ).order_by(
        models.Agents.OrderBy.asc().nullslast(),
        models.Agents.Id.asc(),
    ).all()

    for i in agents:
        results.append(await agent_view_model(db, i))

    return results


@router.get("/fetch_agents", status_code=status.HTTP_200_OK)
async def fetch_agent(
        db: db_dependency,
        episode_id: int,
):
    main_agents, agents_with_assigned_roles = await get_agent_with_roles(db, episode_id)

    return {"Main_Agent": main_agents, "Agents": agents_with_assigned_roles}


@router.get("/fetch_agents_by_role", status_code=status.HTTP_200_OK)
async def fetch_agents_by_role(
        db: db_dependency,
        episode_id: int,
        role: AgentRolesEntities,
):
    results = []

    agents_with_assigned_roles = db.query(
        models.Agents,
        models.AgentRoles,
    ).join(
        models.AgentRoles
    ).where(
        models.Agents.EpisodeId == episode_id,
        models.AgentRoles.Role == role,
    ).order_by(
        models.AgentRoles.OrderBy.asc().nullslast(),
        models.AgentRoles.Id.asc(),
    ).all()

    for agent, role in agents_with_assigned_roles:
        results.append(await agent_view_model(db, agent, role))

    return results


@router.put("/reorder_agents", status_code=status.HTTP_200_OK)
async def reorder_agent(
        db: db_dependency,
        episode_id: int,
        agents_ids: List[int],
):
    agents = db.query(
        models.Agents
    ).where(
        models.Agents.EpisodeId == episode_id,
    ).all()

    for index, agent_id in enumerate(agents_ids):
        for agent in agents:
            if agent.Id == agent_id:
                agent.OrderBy = index

    db.commit()

    return ResponseMessage(
        Error=False,
        Content={
            'Message': 'agents reordered',
        },
    )


@router.put("/reorder_roles", status_code=status.HTTP_200_OK)
async def reorder_agent(
        db: db_dependency,
        episode_id: int,
        role: AgentRolesEntities,
        roles_ids: List[int],
):
    roles = db.query(
        models.AgentRoles
    ).join(
        models.Agents
    ).where(
        models.Agents.EpisodeId == episode_id,
        models.AgentRoles.Role == role.name,
    ).all()

    for index, role_id in enumerate(roles_ids):
        for role in roles:
            if role.Id == role_id:
                role.OrderBy = index

    db.commit()

    return ResponseMessage(
        Error=False,
        Content={
            'Message': f"{role.name}'s agents reordered",
        },
    )


@router.delete("/delete_agent", status_code=status.HTTP_200_OK)
async def delete_agent(
        db: db_dependency,
        agent_id: int,
):
    agent = db.query(models.Agents).where(
        and_(
            models.Agents.Id == agent_id,
        )
    ).first()
    if not agent:
        raise HTTPException(404, "agent not exists!")

    db.delete(agent)
    db.commit()

    return ResponseMessage(
        Error=False,
        Content={
            'Message': 'agent deleted',
        },
    )


@router.delete("/delete_agent_role", status_code=status.HTTP_200_OK)
async def delete_agent_role(
        db: db_dependency,
        role_id: int,
):
    role, agent = db.query(
        models.AgentRoles,
        models.Agents
    ).join(
        models.Agents
    ).where(
        and_(
            models.AgentRoles.Id == role_id,
        )
    ).first()

    if not role or not agent:
        raise HTTPException(404, "agent or role not exists!")

    db.delete(role)
    db.commit()

    return ResponseMessage(
        Error=False,
        Content={
            'Message': 'agent role deleted',
        },
    )
