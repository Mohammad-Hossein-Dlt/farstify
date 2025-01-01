import threading
import time
from datetime import datetime, timedelta
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
import models
from actions_functions.task_actions import cancel_tasks
from database import *
from routers import (
    document,
    ownership,
    agents,
    episode,
    fetch_document,
    categories,
    verify_phone,
    artist,
    artist_profile,
    user,
    user_profile,
    playlist,
    meta_data,
    socials_link,
    file_url,
    task,
    search,
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

app.include_router(file_url.router, prefix=BASE_URL)
app.include_router(search.router, prefix=BASE_URL)
app.include_router(task.router, prefix=BASE_URL)

app.include_router(categories.router, prefix=BASE_URL)
app.include_router(document.router, prefix=BASE_URL)
app.include_router(fetch_document.router, prefix=BASE_URL)
app.include_router(ownership.router, prefix=BASE_URL)
app.include_router(episode.router, prefix=BASE_URL)
app.include_router(agents.router, prefix=BASE_URL)

app.include_router(artist.router, prefix=BASE_URL)
app.include_router(artist_profile.router, prefix=BASE_URL)

app.include_router(verify_phone.router, prefix=BASE_URL)
app.include_router(user.router, prefix=BASE_URL)
app.include_router(user_profile.router, prefix=BASE_URL)
app.include_router(playlist.router, prefix=BASE_URL)

app.include_router(meta_data.router, prefix=BASE_URL)
app.include_router(socials_link.router, prefix=BASE_URL)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
