from pydantic import BaseModel

import models
from fastapi import APIRouter, status
from actions_functions.task_actions import remove_all_tasks_by_artist, remove_single_task_by_artist
from constants import OrderBy
from db_dependency import db_dependency
from actions.response_model import ResponseMessage
from actions.episode_actions import get_episode_short_info
from access_token import artist_token_dependency
from actions.episode_actions import EpisodeFullInfo
from typing import List
router = APIRouter()


class TaskModel(BaseModel):
    id: str
    artistId: int
    episodeId: int
    action_state: str
    creation_date: str


class TaskModesWithEpisode(TaskModel):
    episode: EpisodeFullInfo


# @router.get("/get_artist_tasks", status_code=status.HTTP_200_OK, tags=["Tasks"])
# async def get_artist_tasks(
#         db: db_dependency,
#         artist_id: int,
#         limit: int,
#         page: int,
#         order_by: OrderBy = OrderBy.desc,
# ):
#     # tasks = get_tasks(artist_id=artist_id, limit=limit, page=page, order=order_by)
#     #
#     # episode_ids = set([i.episodeId for i in tasks])
#
#     episodes = db.query(models.Task, models.DocumentsEpisodes, models.Document, models.Artists).join(
#         models.DocumentsEpisodes,
#         models.DocumentsEpisodes.DocumentId == models.Document.Id,
#         isouter=True,
#     ).join(
#         models.Document,
#         models.DocumentsEpisodes.DocumentId == models.Document.Id,
#         isouter=True,
#     ).join(
#         models.Artists,
#         models.Artists.Id == models.Document.Owner,
#         isouter=True,
#     ).where(
#         models.Task.ArtistId == artist_id
#     ).limit(limit).offset(limit * page).all()
#
#     result: List[TaskModesWithEpisode] = []
#
#     for episode, document, artist in episodes:
#         for t in tasks:
#             if episode.Id == t.episodeId:
#                 result.append(
#                     TaskModesWithEpisode(
#                         id=t.id,
#                         artistId=t.artistId,
#                         episodeId=t.episodeId,
#                         action_state=t.action_state,
#                         creation_date=t.creation_date,
#                         episode=await get_episode_short_info(db, episode, document),
#                     )
#                 )
#
#     return result


@router.get("/remove_single_tasks", status_code=status.HTTP_200_OK, tags=["Tasks"])
async def remove_single_tasks(
        access_token: artist_token_dependency,
        task_id: int,
):
    remove_single_task_by_artist(db=db_dependency, artist_id=access_token.user_id, task_id=task_id)
    return ResponseMessage(error=False, message="task deleted!")


@router.get("/remove_all_tasks", status_code=status.HTTP_200_OK, tags=["Tasks"])
async def remove_all_tasks(
        access_token: artist_token_dependency,
):
    remove_all_tasks_by_artist(db=db_dependency, artist_id=access_token.user_id)
    return ResponseMessage(error=False, message="all tasks deleted!")
