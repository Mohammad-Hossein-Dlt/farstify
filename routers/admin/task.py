from pydantic import BaseModel
from fastapi import APIRouter, status
from actions_functions.task_actions import remove_all_tasks, remove_single_task
from actions.response_model import ResponseMessage
from db_dependency import db_dependency

router = APIRouter(prefix="/task", tags=["Admin-Tasks"])


class TaskModel(BaseModel):
    id: str
    artistId: int
    episodeId: int
    action_state: str
    creation_date: str


@router.get("/delete_single_task", status_code=status.HTTP_200_OK)
async def delete_task(
        db: db_dependency,
        task_id: int,
):
    remove_single_task(db=db, task_id=task_id)
    return ResponseMessage(
        Error=False,
        Content={
            'Message': 'task deleted',
        },
    )


@router.get("/remove_all_tasks", status_code=status.HTTP_200_OK)
async def remove_tasks(
        db: db_dependency,
        episode_id: int,
):
    remove_all_tasks(db=db, episode_id=episode_id)
    return ResponseMessage(
        Error=False,
        Content={
            'Message': 'all tasks deleted',
        },
    )
