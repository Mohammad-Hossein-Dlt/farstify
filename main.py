import asyncio
from datetime import datetime, timedelta
from fastapi import FastAPI
from contextlib import asynccontextmanager
import models
from actions_functions.task_actions import cancel_tasks
from database import *
from routers import (
    document,
    contributors,
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
    home_page,
    meta_data,
    socials_link,
    file_url,
    task,
    search,
)


async def do_update():
    db = sessionLocal()

    time_period = datetime.now() - timedelta(minutes=5)

    junk_user_temps = db.query(models.UsersTemp).where(
        models.UsersTemp.Date < time_period
    ).all()

    for i in junk_user_temps:
        db.delete(i)

    # junk_following = db.query(models.UserFollowing).where(
    #     and_(
    #         models.UserFollowing.ArtistId == None,
    #         models.UserFollowing.DocumentId == None,
    #         models.UserFollowing.PlayListId == None,
    #     )
    # ).all()
    #
    # for i in junk_following:
    #     db.delete(i)

    db.commit()

    db.close()

    await cancel_tasks()

    print("Task done.")


async def repeat():
    while True:
        asyncio.create_task(do_update())
        await asyncio.sleep(1000)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Start up.")
    create_directories()
    # create_db()
    models.Base.metadata.create_all(bind=engine)
    asyncio.create_task(repeat())
    yield
    print("Shout down.")


app = FastAPI(lifespan=lifespan)
app.title = "Farstify"

BASE_URL = "/api/v2"

app.include_router(file_url.router, prefix=BASE_URL)
app.include_router(search.router, prefix=BASE_URL)
app.include_router(task.router, prefix=BASE_URL)
app.include_router(document.router, prefix=BASE_URL)
app.include_router(contributors.router, prefix=BASE_URL)
app.include_router(agents.router, prefix=BASE_URL)
app.include_router(episode.router, prefix=BASE_URL)
app.include_router(fetch_document.router, prefix=BASE_URL)
app.include_router(categories.router, prefix=BASE_URL)
app.include_router(verify_phone.router, prefix=BASE_URL)
app.include_router(artist.router, prefix=BASE_URL)
app.include_router(artist_profile.router, prefix=BASE_URL)
app.include_router(user.router, prefix=BASE_URL)
app.include_router(user_profile.router, prefix=BASE_URL)
app.include_router(playlist.router, prefix=BASE_URL)
app.include_router(home_page.router, prefix=BASE_URL)
app.include_router(meta_data.router, prefix=BASE_URL)
app.include_router(socials_link.router, prefix=BASE_URL)
