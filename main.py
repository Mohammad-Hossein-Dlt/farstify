import threading
import time
from datetime import datetime, timedelta
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
import models
from actions_functions.task_actions import cancel_tasks
from database import *
from routers.admin import (
    agents as admin_agents,
    artist as admin_artist,
    categories as admin_categories,
    document as admin_document,
    episode as admin_episode,
    meta_data as admin_meta_data,
    ownership as admin_ownership,
    socials_link as admin_socials_link,
    task as admin_task,
)

from routers.general import (
    artist as general_artist,
    categories as general_categories,
    document as general_document,
    episode as general_episode,
    file_url as general_file_url,
    playlist as general_playlist,
    search as general_search,
    verify_phone as general_verify_phone,
)

from routers.user import (
    authentication as user_authentication,
    follow as user_follow,
    like as user_like,
    playlist as user_playlist,
    profile as user_profile,
)


def delete_users_temps():
    db = sessionLocal()

    time_period = datetime.now() - timedelta(minutes=5)

    junk_user_temps = db.query(models.UsersTemp).where(
        models.UsersTemp.Date < time_period
    ).all()

    for i in junk_user_temps:
        db.delete(i)

    db.commit()
    db.close()


def delete_junk_following():
    db = sessionLocal()

    junk_following = db.query(models.UserFollowing).where(
        models.UserFollowing.ArtistId.is_(None),
        models.UserFollowing.DocumentId.is_(None),
        models.UserFollowing.PlayListId.is_(None),
    ).all()

    for i in junk_following:
        db.delete(i)

    db.commit()
    db.close()


def do_update():
    while True:
        delete_users_temps()
        delete_junk_following()
        cancel_tasks()
        print("Task Done.")
        time.sleep(300)


def start_update():
    threading.Thread(target=do_update).start()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Start up.")
    create_directories()
    # create_db()
    models.Base.metadata.create_all(bind=engine)
    # start_update()
    yield
    print("Shout down.")


app = FastAPI(lifespan=lifespan)
app.title = "Farstify"

BASE_URL = "/api/v2"

app.include_router(general_file_url.router, prefix=BASE_URL)
app.include_router(admin_task.router, prefix=BASE_URL)

app.include_router(admin_artist.router, prefix=BASE_URL)
app.include_router(admin_categories.router, prefix=BASE_URL)
app.include_router(admin_document.router, prefix=BASE_URL)
app.include_router(admin_ownership.router, prefix=BASE_URL)
app.include_router(admin_episode.router, prefix=BASE_URL)
app.include_router(admin_agents.router, prefix=BASE_URL)
app.include_router(admin_meta_data.router, prefix=BASE_URL)
app.include_router(admin_socials_link.router, prefix=BASE_URL)

app.include_router(general_artist.router, prefix=BASE_URL)
app.include_router(general_categories.router, prefix=BASE_URL)
app.include_router(general_document.router, prefix=BASE_URL)
app.include_router(general_episode.router, prefix=BASE_URL)
app.include_router(general_playlist.router, prefix=BASE_URL)
app.include_router(general_search.router, prefix=BASE_URL)
app.include_router(general_verify_phone.router, prefix=BASE_URL)


app.include_router(user_authentication.router, prefix=BASE_URL)
app.include_router(user_profile.router, prefix=BASE_URL)
app.include_router(user_playlist.router, prefix=BASE_URL)
app.include_router(user_follow.router, prefix=BASE_URL)
app.include_router(user_like.router, prefix=BASE_URL)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
