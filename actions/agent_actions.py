from pydantic import BaseModel
from actions.artist_short_info_actions import ArtistShortInfo, get_artist_short_info
from db_dependency import db_dependency
from models import Agents, Artists
from typing import List, Dict
from constants import AgentRolesEntities


class AgentViewMode(BaseModel):
    id: int | None = None
    name: str | None = None
    profile: ArtistShortInfo | None = None
    is_main: bool = False
    order: int | None = None


async def agent_view_model(
        db: db_dependency,
        agent: Agents,
) -> AgentViewMode:
    data = AgentViewMode()
    data.id = agent.Id
    data.name = agent.Name
    if agent.ArtistId:
        artist = db.query(Artists).where(Artists.Id == agent.ArtistId).first()
        data.profile = get_artist_short_info(artist)
        data.name = artist.Name

    data.is_main = agent.IsMain
    data.order = agent.OrderBy

    return data


async def get_main_agent(
        db: db_dependency,
        artist_list: List[Agents],
):
    roles = [AgentRolesEntities.Main_Artist, AgentRolesEntities.Featured_Artist]

    main_agents: List = list()

    for agent in artist_list:
        new_agent = await agent_view_model(db, agent)
        if agent.IsMain:
            agent_roles = [i.Role for i in agent.roles if i.Role in roles]
            main_agents.append([new_agent, agent_roles])

    return main_agents


async def get_agent_with_roles(
        db: db_dependency,
        artist_list: List[Agents],
):
    main_agents: List = list()
    given_role_agents: Dict[str, list] = dict()

    for agent in artist_list:
        new_agent = await agent_view_model(db, agent)
        if agent.IsMain:
            agent_roles = [i.Role for i in agent.roles]
            main_agents.append([new_agent, agent_roles])

    for role in AgentRolesEntities:
        agents_with_i_role: List[AgentViewMode] = list()
        for agent in artist_list:
            agent_roles = {i.Role: i.OrderBy for i in agent.roles}
            if agent_roles.keys().__contains__(role):
                new_agent = await agent_view_model(db, agent)
                order = agent_roles.get(role)
                new_agent.order = order
                agents_with_i_role.append(new_agent)

        null_orders: List[AgentViewMode] = list()
        none_null_orders: List[AgentViewMode] = list()
        for i in agents_with_i_role:
            if i.order is None:
                null_orders.append(i)
            else:
                none_null_orders.append(i)

        for index in range(len(none_null_orders)):
            min_index = index
            for j in range(index + 1, len(none_null_orders)):
                a = none_null_orders[j].order
                b = none_null_orders[min_index].order
                if (a is not None and b is not None) and (a < b):
                    min_index = j
            none_null_orders[min_index], none_null_orders[index] = none_null_orders[index], none_null_orders[min_index]

        for index in range(len(null_orders)):
            min_index = index
            for j in range(index + 1, len(null_orders)):
                a = null_orders[j].id
                b = null_orders[min_index].id
                if (a is not None and b is not None) and (a < b):
                    min_index = j
            null_orders[min_index], null_orders[index] = null_orders[index], null_orders[min_index]

        given_role_agents.update({role: [*none_null_orders, *null_orders]})

    return main_agents, given_role_agents
