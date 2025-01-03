from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy import and_, or_
from database import sessionLocal
from db_dependency import db_dependency
from constants import ProcessActionTaskState
import models


def add_processing_task(
        episode_id: int,
) -> int:
    db = sessionLocal()

    check = db.query(
        models.Task
    ).where(
        and_(
            models.Task.EpisodeId == episode_id,
            or_(
                models.Task.ActionState == ProcessActionTaskState.launching,
                models.Task.ActionState == ProcessActionTaskState.in_process,
            ),
        ),
    ).first()

    if not check:
        new_task = models.Task()
        new_task.EpisodeId = episode_id
        new_task.ActionState = ProcessActionTaskState.launching

        db.add(new_task)

        db.commit()
        db.refresh(new_task)

        db.close()
        return new_task.Id
    else:
        db.close()
        raise HTTPException(403, "previous upload is in processing")


def update_task(
        task_id: int,
        state: ProcessActionTaskState,
) -> int:
    db = sessionLocal()

    task = db.query(
        models.Task
    ).where(
        models.Task.Id == task_id,
    ).first()

    if task:
        task.ActionState = state

        db.commit()
        db.refresh(task)
        db.close()
        return task.Id
    else:
        db.close()
        raise HTTPException(403, "no task exist")


async def check_task_in_process(
        episode_id: int,
) -> bool:
    db = sessionLocal()

    task = db.query(
        models.Task
    ).where(
        and_(
            models.Task.EpisodeId == episode_id,
            or_(
                models.Task.ActionState == ProcessActionTaskState.launching,
                models.Task.ActionState == ProcessActionTaskState.in_process,
            )
        )
    ).first()

    if task:
        return True

    return False


def cancel_tasks():
    time_period = datetime.now() - timedelta(minutes=30)

    db = sessionLocal()

    tasks = db.query(
        models.Task
    ).where(
        and_(
            models.Task.CreationDate < time_period,
            or_(
                models.Task.ActionState == ProcessActionTaskState.launching,
                models.Task.ActionState == ProcessActionTaskState.in_process,
            ),
        )
    ).all()

    for i in tasks:
        i.ActionState = ProcessActionTaskState.error

    db.commit()

    db.close()


def remove_all_tasks(
        db: db_dependency,
        episode_id: int,
):
    tasks = db.query(
        models.Task
    ).where(
        models.Task.EpisodeId == episode_id,
    ).all()

    for i in tasks:
        db.delete(i)

    db.commit()


def remove_single_task(
        db: db_dependency,
        task_id: int,
):
    task = db.query(
        models.Task
    ).where(
        models.Task.Id == task_id,
    ).first()

    db.delete(task)

    db.commit()
