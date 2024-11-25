import models
import time
import uuid
import pathlib
import shutil
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from access_token import optional_user_token_dependency
from moviepy.editor import AudioFileClip
from fastapi import APIRouter, BackgroundTasks, HTTPException, status, UploadFile, File
from sqlalchemy import and_
from actions_functions.task_actions import add_processing_task, update_task, check_task_in_process
from database import sessionLocal
from storage import storage, Buckets, storage_delete_file
from utills.temp import manual_delete_temp_dependency
from db_dependency import db_dependency
from utills.path_manager import make_path
from utills.exceptions import owned_exception
from utills.check_ownership import is_document_owned_by_artist, is_episode_owned_by_artist
from utills.check_follow import liked_episode
from constants import DocumentQualities, ProcessActionTaskState
from actions.response_model import ResponseMessage
from actions.episode_actions import get_episode_full_info, get_episode_short_info

router = APIRouter()


def make_qualities(
        # db: db_dependency,
        temp: manual_delete_temp_dependency,
        artist_id: int,
        episode_id: int,
        document_directory: str,
        new_file_name: str,
        previous_file_name: str | None = None,
):
    t1 = time.monotonic()

    task = add_processing_task(artist_id=artist_id, episode_id=episode_id)

    # if not task:
    #     raise HTTPException(403, "previous upload is in processing")
    print("////////////////")
    print(task)
    update_task(task, ProcessActionTaskState.in_process)

    audio_path = make_path(temp.path, new_file_name, is_file=True)

    async def remove_from_storage(file_name: storage):
        try:
            for directory in DocumentQualities.directories():
                file_path = make_path(document_directory, directory, file_name, is_file=True)
                storage_delete_file(file_path, Buckets.DOCUMENT_BUCKET_NAME)

        except Exception as ex4:
            print(ex4)
            update_task(task, ProcessActionTaskState.error)
        else:
            pass
            temp.delete()

    try:
        audio = AudioFileClip(audio_path)
    except Exception as ex:
        print(ex)
        temp.delete()
        update_task(task, ProcessActionTaskState.error)
    else:
        try:
            s = time.monotonic()

            def audio_converter(quality: str):
                raw_audio = AudioFileClip(audio_path)
                new_path = make_path(temp.path, quality, new_file_name, is_file=True)
                raw_audio.write_audiofile(
                    new_path,
                    bitrate=quality,
                    codec="libmp3lame",
                )

            # with ThreadPoolExecutor(max_workers=os.cpu_count()) as pool:
            with ThreadPoolExecutor(max_workers=2) as pool:
                futures = [pool.submit(audio_converter, q) for q in DocumentQualities.qualities()]
                for future in as_completed(futures):
                    print(future.result())

            e = time.monotonic()
            print("Processing (Seconds)=================: " + str(round(e - s, 2)))
            print("Processing (Minutes)=================: " + str(round((e - s) / 60, 2)))

            preview_path = make_path(temp.path, DocumentQualities.preview, new_file_name, is_file=True)

            duration = audio.duration
            clipped = audio.subclip(0, duration * 0.2)
            clipped.write_audiofile(preview_path, codec="libmp3lame")

            clipped.close()
            audio.close()

        except Exception as ex1:
            print(ex1)
            audio.close()
            temp.delete()
            update_task(task, ProcessActionTaskState.error)
        else:
            try:
                for q_directory in DocumentQualities.directories():
                    temp_file = make_path(temp.path, q_directory, new_file_name, is_file=True)
                    storage_file = make_path(document_directory, q_directory, new_file_name, is_file=True)
                    with open(temp_file, "rb") as file:
                        storage.upload_fileobj(file, Bucket=Buckets.DOCUMENT_BUCKET_NAME, Key=storage_file)
                        file.close()
                    print(temp_file)
            except Exception as ex2:
                print(ex2)
                update_task(task, ProcessActionTaskState.error)
                remove_from_storage(new_file_name)
            else:
                try:
                    static_db = sessionLocal()
                    episode, document = static_db.query(models.DocumentsEpisodes, models.Document).join(
                        models.Document,
                    ).where(
                        models.DocumentsEpisodes.Id == episode_id,
                    ).first()
                    episode.File = new_file_name
                    episode.Duration = round(duration)
                    static_db.commit()

                    update_task(task, ProcessActionTaskState.completed)
                    remove_from_storage(previous_file_name)

                    static_db.close()
                except Exception as ex3:
                    print(ex3)
                    update_task(task, ProcessActionTaskState.error)
                    remove_from_storage(new_file_name)
                    print("@@@@@@@@@@@@@@@@@@")

    temp.delete()
    t2 = time.monotonic()
    print("Seconds: " + str(round(t2 - t1, 2)))
    print("Minutes: " + str(round((t2 - t1) / 60, 2)))


async def create_preview(
        artist_id: int,
        document: models.Document,
        episode: models.DocumentsEpisodes,
        temp: manual_delete_temp_dependency,
        start_second: int,
        end_second: int,
):
    task = add_processing_task(artist_id=artist_id, episode_id=episode.Id)

    # if not task:
    #     temp.delete()
    #     raise HTTPException(403, "previous upload is in processing")

    update_task(task, ProcessActionTaskState.in_process)

    try:
        storage_320k_path = make_path(
            document.DirectoryName,
            DocumentQualities.q320k_bit,
            episode.File,
            is_file=True,
        )

        download_path = make_path(temp.path, "main-" + episode.File, is_file=True)
        temp_path = make_path(
            temp.path,
            episode.File,
            is_file=True,
        )

        storage_preview_path = make_path(
            document.DirectoryName,
            DocumentQualities.preview,
            episode.File,
            is_file=True
        )
        print("Download in: ", download_path)

        storage.download_file(Buckets.DOCUMENT_BUCKET_NAME, storage_320k_path, download_path)

        audio = AudioFileClip(download_path)

        duration = audio.duration

        start = min(max(start_second, 0), duration)

        end = min(max(end_second, 0), duration)

        if start >= end:
            end = duration

        clipped = audio.subclip(start, end)

        clipped.write_audiofile(temp_path)

        clipped.close()
        audio.close()

        print("Upload from: ", temp_path)
        with open(temp_path, "rb") as file:
            storage.upload_fileobj(file, Bucket=Buckets.DOCUMENT_BUCKET_NAME, Key=storage_preview_path)
            file.close()
    except Exception as ex:
        print(ex)
        update_task(task, ProcessActionTaskState.error)
        temp.delete()
    else:
        print("Process Done.")
        update_task(task, ProcessActionTaskState.completed)
        temp.delete()


@router.post("/create-episode", status_code=status.HTTP_201_CREATED, tags=["Episode"])
async def create_episode(
        db: db_dependency,
        artist_id: int,
        document_id: int,
        episode_id: int | None = None,
        title: str | None = None,
        image_file: UploadFile = File(None),
        delete_image: bool = False,
):
    if not await is_document_owned_by_artist(db, document_id=document_id, artist_id=artist_id):
        raise owned_exception

    async def upload_image(previous_file_name: str | None) -> str:

        the_document = db.query(models.Document).where(models.Document.Id == document_id).first()

        new_file_name = uuid.uuid4().hex + pathlib.Path(image_file.filename).suffix

        image_path = make_path(the_document.DirectoryName, new_file_name, is_file=True)

        try:

            storage.upload_fileobj(image_file.file, Bucket=Buckets.DOCUMENT_BUCKET_NAME, Key=image_path)

        except Exception as ex:
            print(ex)
        else:
            if previous_file_name:
                try:
                    image_path = make_path(the_document.DirectoryName, previous_file_name, is_file=True)
                    storage_delete_file(image_path, Buckets.DOCUMENT_BUCKET_NAME)

                except Exception as ex:
                    print(ex)

        return new_file_name

    if episode_id:
        ep = db.query(models.DocumentsEpisodes).where(
            and_(
                models.DocumentsEpisodes.Id == episode_id,
                models.DocumentsEpisodes.DocumentId == document_id
            )
        ).first()

        if not ep:
            raise HTTPException(404, "Episode not found!")

        ep.Title = title if title else ep.Title

        if image_file:
            ep.Image = await upload_image(ep.Image)
        elif delete_image:
            try:
                document = db.query(models.Document).select_from(models.DocumentsEpisodes).where(
                    models.DocumentsEpisodes.Id == episode_id,
                    models.DocumentsEpisodes.DocumentId == document_id).first()
                path = make_path(document.DirectoryName, ep.Image, is_file=True)
                storage_delete_file(path, Buckets.DOCUMENT_BUCKET_NAME)

            except Exception as ex:
                print(ex)
            else:
                ep.Image = None

        db.commit()

        return ResponseMessage(error=False, message="Episode updated!")
    else:
        ep = {"DocumentId": document_id, "Title": title}
        ep = models.DocumentsEpisodes(**ep)
        if image_file:
            ep.Image = await upload_image(None)
        db.add(ep)
        db.commit()

        return ResponseMessage(error=False, message="New episode created!")


@router.post("/upload-episode-file", status_code=status.HTTP_201_CREATED, tags=["Episode"])
async def upload_episode_file(
        db: db_dependency,
        artist_id: int,
        temp: manual_delete_temp_dependency,
        episode_id: int,
        audio_file: UploadFile,
        background_tasks: BackgroundTasks = BackgroundTasks(),
):
    print("........................................................")

    if await check_task_in_process(artist_id=artist_id, episode_id=episode_id):
        temp.delete()
        raise HTTPException(403, "previous upload is in processing")

    if not await is_episode_owned_by_artist(db, episode_id=episode_id, artist_id=artist_id):
        raise owned_exception

    episode, document = db.query(models.DocumentsEpisodes, models.Document).join(
        models.Document
    ).where(
        and_(
            models.DocumentsEpisodes.Id == episode_id,
        )
    ).first()

    if not episode:
        return ResponseMessage(error=True, message="No episode exist!")

    name_mp3 = temp.name + ".mp3"
    path_mp3 = make_path(temp.path, name_mp3, is_file=True)

    for i in DocumentQualities.directories():
        p = make_path(temp.path, i, is_file=False)
        if not os.path.exists(p):
            os.mkdir(p)

    with open(path_mp3, "wb") as f:
        shutil.copyfileobj(audio_file.file, f)
        f.write(await audio_file.read())

    background_tasks.add_task(
        make_qualities,
        # db,
        temp,
        artist_id,
        episode.Id,
        document.DirectoryName,
        name_mp3,
        episode.File,
    )
    return ResponseMessage(error=False, message="Episode file on processing...")


@router.post("/edit-temp", status_code=status.HTTP_201_CREATED, tags=["Episode"])
async def edit_temp(
        db: db_dependency,
        artist_id: int,
        temp: manual_delete_temp_dependency,
        episode_id: int,
        start_second: int,
        end_second: int,
        background_tasks: BackgroundTasks = BackgroundTasks(),
):
    episode, document = db.query(models.DocumentsEpisodes, models.Document).join(
        models.Document
    ).where(
        models.DocumentsEpisodes.Id == episode_id
    ).first()

    if not await is_document_owned_by_artist(db, document_id=document.Id, artist_id=artist_id):
        raise owned_exception

    if await check_task_in_process(artist_id=artist_id, episode_id=episode_id):
        temp.delete()
        raise HTTPException(403, "previous upload is in processing")

    background_tasks.add_task(
        create_preview,
        artist_id,
        document,
        episode,
        temp,
        start_second,
        end_second
    )

    return ResponseMessage(error=False, message="New temp episode created!")


@router.get("/fetch-single-episode", status_code=status.HTTP_201_CREATED, tags=["Episode"])
async def fetch_single_episode(
        db: db_dependency,
        document_id: int,
        episode_id: int,
        access_token: optional_user_token_dependency,
):
    the_episode = db.query(models.DocumentsEpisodes).where(models.DocumentsEpisodes.Id == episode_id,
                                                           models.DocumentsEpisodes.DocumentId == document_id).first()
    the_document = db.query(models.Document).where(models.Document.Id == document_id).first()

    if the_episode is None or the_document is None:
        raise HTTPException(404, "an error occurred!")

    episode_info = await get_episode_full_info(db=db, episode=the_episode, document=the_document)

    if access_token.permission:
        episode_info.Followed = liked_episode(db=db, user_id=access_token.user_id, episode_id=the_episode.Id)

    return episode_info


@router.get("/fetch-all-episodes", status_code=status.HTTP_201_CREATED, tags=["Episode"])
async def fetch_all_episodes(
        db: db_dependency,
        document_id: int,
        limit: int, page: int,
):
    result = []
    episodes = db.query(models.DocumentsEpisodes).where(models.DocumentsEpisodes.DocumentId == document_id).limit(
        limit).offset(limit * page).all()
    document = db.query(models.Document).where(models.Document.Id == document_id).first()

    # artist = db.query(models.Artists).where(models.Artists.Id == document.Owner).first()

    if document is None:
        raise HTTPException(404, "an error occurred!")

    for i in episodes:
        result.append(await get_episode_short_info(db=db, episode=i, document=document))

    return result


@router.delete("/delete-episodes", status_code=status.HTTP_200_OK, tags=["Episode"])
async def delete_episodes(
        db: db_dependency,
        artist_id: int,
        document_id: int,
        episodes_id: int,
):
    if not await is_document_owned_by_artist(db, document_id=document_id, artist_id=artist_id):
        raise owned_exception

    the_episode = db.query(models.DocumentsEpisodes).where(models.DocumentsEpisodes.Id == episodes_id).first()
    if document_id == the_episode.DocumentId:
        the_document = db.query(models.Document).where(models.Document.Id == document_id).first()
        try:
            path = make_path(the_document.DirectoryName, is_file=False)

            audio_file = make_path(path, the_episode.File, is_file=True)
            storage_delete_file(audio_file, Buckets.DOCUMENT_BUCKET_NAME)

            preview_path = make_path(path, DocumentQualities.preview, the_episode.File, is_file=True)
            storage_delete_file(preview_path, Buckets.DOCUMENT_BUCKET_NAME)

            for i in DocumentQualities.directories():
                p = make_path(path, i, the_episode.File, is_file=True)
                storage_delete_file(p, Buckets.DOCUMENT_BUCKET_NAME)

            imageFile = make_path(path, the_episode.Image, is_file=True)
            storage_delete_file(imageFile, Buckets.DOCUMENT_BUCKET_NAME)
        except Exception as ex:
            print(ex)
        else:
            db.delete(the_episode)
            db.commit()

            return ResponseMessage(error=False, message="Episode deleted!")
