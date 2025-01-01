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
from utills.parse_null import pars_null
from utills.temp import manual_delete_temp_dependency
from db_dependency import db_dependency
from utills.path_manager import make_path
from utills.check_follow import liked_episode
from constants import DocumentQualities, ProcessActionTaskState
from actions.response_model import ResponseMessage
from actions.episode_actions import get_episode_full_info, get_episode_short_info

router = APIRouter(prefix="/episode", tags=["Episode"])


def make_qualities(
        temp: manual_delete_temp_dependency,
        episode_id: int,
        document_directory: str,
        new_file_name: str,
        previous_file_name: str | None = None,
):
    task = add_processing_task(episode_id=episode_id)
    update_task(task, ProcessActionTaskState.in_process)
    audio_path = make_path(
        temp.path,
        new_file_name,
        is_file=True
    )

    def remove_from_storage(file_name: storage):
        try:
            print("deleting previous files...")
            for directory in DocumentQualities.directories():
                file_path = make_path(
                    document_directory,
                    directory,
                    file_name,
                    is_file=True,
                )
                storage_delete_file(file_path, Buckets.DOCUMENT_BUCKET_NAME)
            print("deleting previous files was complete...")

        except Exception as ex4:
            print(ex4)
            update_task(task, ProcessActionTaskState.error)
        else:
            temp.delete()

    try:
        audio = AudioFileClip(audio_path)
    except Exception as ex:
        print(ex)
        temp.delete()
        update_task(task, ProcessActionTaskState.error)
    else:
        print("Creating qualities...")
        try:
            def audio_converter(quality: str):
                raw_audio = AudioFileClip(audio_path)
                new_path = make_path(temp.path, quality, new_file_name, is_file=True)
                raw_audio.write_audiofile(
                    new_path,
                    bitrate=quality,
                    codec="libmp3lame",
                    logger=None,
                )
                raw_audio.close()

            with ThreadPoolExecutor(max_workers=os.cpu_count()) as pool:
                # with ThreadPoolExecutor(max_workers=2) as pool:
                futures = [pool.submit(audio_converter, q) for q in DocumentQualities.qualities()]
                for future in as_completed(futures):
                    print(future.result())

            preview_path = make_path(
                temp.path,
                DocumentQualities.preview,
                new_file_name,
                is_file=True
            )

            duration = audio.duration
            clipped = audio.subclip(0, duration * 0.2)
            clipped.write_audiofile(
                preview_path,
                codec="libmp3lame",
                logger=None,
            )

            clipped.close()
            audio.close()

        except Exception as ex1:
            print(ex1)
            audio.close()
            temp.delete()
            update_task(task, ProcessActionTaskState.error)
        else:
            print("Creating qualities was complete...")
            print("uploading qualities...")
            try:
                for q_directory in DocumentQualities.directories():
                    temp_file = make_path(
                        temp.path,
                        q_directory,
                        new_file_name,
                        is_file=True
                    )

                    storage_file = make_path(
                        document_directory,
                        q_directory,
                        new_file_name,
                        is_file=True
                    )

                    with open(temp_file, "rb") as file:
                        storage.upload_fileobj(file, Bucket=Buckets.DOCUMENT_BUCKET_NAME, Key=storage_file)
                        file.close()

            except Exception as ex2:
                print(ex2)
                update_task(task, ProcessActionTaskState.error)
                remove_from_storage(new_file_name)
            else:
                print("uploading qualities was complete...")
                try:
                    db = sessionLocal()
                    episode = db.query(
                        models.DocumentsEpisodes,
                    ).where(
                        models.DocumentsEpisodes.Id == episode_id,
                    ).first()
                    episode.File = new_file_name
                    episode.Duration = round(duration)
                    update_task(task, ProcessActionTaskState.completed)
                    remove_from_storage(previous_file_name)
                    db.commit()
                    db.close()
                except Exception as ex3:
                    print(ex3)
                    update_task(task, ProcessActionTaskState.error)
                    remove_from_storage(new_file_name)

    temp.delete()

    print("finish process")


async def create_preview(
        document: models.Document,
        episode: models.DocumentsEpisodes,
        temp: manual_delete_temp_dependency,
        start_second: int,
        end_second: int,
):
    task = add_processing_task(episode_id=episode.Id)
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


@router.post("/insert_episode", status_code=status.HTTP_201_CREATED)
async def create_episode(
        db: db_dependency,
        document_id: int,
        episode_id: int | None = None,
        title: str | None = None,
        image_file: UploadFile = File(None),
        delete_image: bool = False,
):
    episode_id = pars_null(episode_id)
    title = pars_null(title)

    async def upload_image(previous_file_name: str | None, directoryName: str) -> str:
        new_file_name = uuid.uuid4().hex + pathlib.Path(image_file.filename).suffix
        image_path = make_path(directoryName, new_file_name, is_file=True)
        try:
            storage.upload_fileobj(image_file.file, Bucket=Buckets.DOCUMENT_BUCKET_NAME, Key=image_path)
        except Exception as ex:
            print(ex)
        else:
            if previous_file_name:
                try:
                    image_path = make_path(directoryName, previous_file_name, is_file=True)
                    storage_delete_file(image_path, Buckets.DOCUMENT_BUCKET_NAME)
                except Exception as ex:
                    print(ex)
        return new_file_name

    if episode_id:

        document, episode = db.query(
            models.Document,
            models.DocumentsEpisodes
        ).join(
            models.DocumentsEpisodes,
        ).where(
            models.DocumentsEpisodes.Id == episode_id,
        ).first()

        if not episode:
            raise HTTPException(404, "the episode not found!")

        episode.Title = title if title else episode.Title

        if image_file:
            episode.Image = await upload_image(episode.Image, document.DirectoryName)
        elif delete_image:
            try:
                path = make_path(document.DirectoryName, episode.Image, is_file=True)
                storage_delete_file(path, Buckets.DOCUMENT_BUCKET_NAME)
            except Exception as ex:
                print(ex)
            else:
                episode.Image = None

        db.commit()

        response = {"Episode_Id": episode.Id}
    else:

        document = db.query(
            models.Document,
        ).where(
            models.Document == document_id,
        ).first()

        episode = models.DocumentsEpisodes()

        episode.DocumentId = document_id
        episode.Title = title

        if image_file:
            episode.Image = await upload_image(None, document.DirectoryName)
        db.add(episode)
        db.commit()

        response = {"Episode_Id": episode.Id}

    db.commit()
    return response


@router.post("/upload_episode_file", status_code=status.HTTP_201_CREATED)
async def upload_episode_file(
        db: db_dependency,
        temp: manual_delete_temp_dependency,
        episode_id: int,
        audio_file: UploadFile,
        background_tasks: BackgroundTasks = BackgroundTasks(),
):
    if await check_task_in_process(episode_id=episode_id):
        temp.delete()
        raise HTTPException(403, "previous upload is in processing")

    document, episode = db.query(
        models.Document,
        models.DocumentsEpisodes,
    ).join(
        models.Document
    ).where(
        models.DocumentsEpisodes.Id == episode_id,
    ).first()

    if not document or not episode:
        raise HTTPException(404, "document or episode not found!")

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
        episode.Id,
        document.DirectoryName,
        name_mp3,
        episode.File,
    )
    return ResponseMessage(error=False, message="episode file is in processing...")


@router.post("/edit_temp", status_code=status.HTTP_201_CREATED)
async def edit_temp(
        db: db_dependency,
        temp: manual_delete_temp_dependency,
        episode_id: int,
        start_second: int,
        end_second: int,
        background_tasks: BackgroundTasks = BackgroundTasks(),
):
    episode, document = db.query(
        models.DocumentsEpisodes,
        models.Document
    ).join(
        models.Document
    ).where(
        models.DocumentsEpisodes.Id == episode_id
    ).first()

    if await check_task_in_process(episode_id=episode_id):
        temp.delete()
        raise HTTPException(403, "previous upload is in processing!")

    if not document or not episode:
        raise HTTPException(404, "document or episode not found!")

    background_tasks.add_task(
        create_preview,
        document,
        episode,
        temp,
        start_second,
        end_second
    )

    return ResponseMessage(error=False, message="new temp episode is in creating...")


@router.delete("/delete_episode_file", status_code=status.HTTP_200_OK)
async def delete_episode_file(
        db: db_dependency,
        episode_id: int,
):
    the_document, the_episode = db.query(
        models.Document,
        models.DocumentsEpisodes
    ).join(
        models.DocumentsEpisodes
    ).where(
        models.DocumentsEpisodes.Id == episode_id,
    ).first()

    if not the_document or not the_episode:
        raise HTTPException(403, "document or episode not found!")

    try:
        path = make_path(the_document.DirectoryName, is_file=False)
        preview_path = make_path(path, DocumentQualities.preview, the_episode.File, is_file=True)
        storage_delete_file(preview_path, Buckets.DOCUMENT_BUCKET_NAME)
        for i in DocumentQualities.directories():
            p = make_path(path, i, the_episode.File, is_file=True)
            storage_delete_file(p, Buckets.DOCUMENT_BUCKET_NAME)
    except Exception as ex:
        print(ex)
        raise HTTPException(500, "unable to delete the episode file completely!")
    else:
        the_episode.File = None
        the_episode.Duration = 0
        db.commit()
        return ResponseMessage(error=False, message="episode file deleted")


@router.get("/fetch_single_episode", status_code=status.HTTP_201_CREATED)
async def fetch_single_episode(
        db: db_dependency,
        episode_id: int,
        access_token: optional_user_token_dependency,
):
    the_document, the_episode = db.query(
        models.Document,
        models.DocumentsEpisodes
    ).join(
        models.Document
    ).where(
        models.DocumentsEpisodes.Id == episode_id,
    ).first()

    if not the_episode or not the_document:
        raise HTTPException(404, "document or episode not found!")

    episode_info = await get_episode_full_info(db=db, episode=the_episode, document=the_document)

    if access_token.permission:
        episode_info.Followed = liked_episode(db=db, user_id=access_token.user_id, episode_id=the_episode.Id)

    return episode_info


@router.get("/fetch_all_episodes", status_code=status.HTTP_201_CREATED)
async def fetch_all_episodes(
        db: db_dependency,
        document_id: int,
        limit: int,
        page: int,
        access_token: optional_user_token_dependency,
):
    result = []

    episodes = db.query(
        models.DocumentsEpisodes
    ).where(
        models.DocumentsEpisodes.DocumentId == document_id
    ).limit(
        limit
    ).offset(
        limit * page
    ).all()

    document = db.query(
        models.Document
    ).where(
        models.Document.Id == document_id
    ).first()

    if document is None:
        raise HTTPException(404, "document not found!")

    for i in episodes:
        episode = await get_episode_short_info(db=db, episode=i, document=document)

        if access_token.permission:
            episode.Followed = liked_episode(db=db, user_id=access_token.user_id, episode_id=episode.Id)

        result.append(episode)

    return result


@router.delete("/delete_episode", status_code=status.HTTP_200_OK)
async def delete_episode(
        db: db_dependency,
        episode_id: int,
):
    the_document, the_episode = db.query(
        models.Document,
        models.DocumentsEpisodes
    ).join(
        models.DocumentsEpisodes
    ).where(
        models.DocumentsEpisodes.Id == episode_id,
    ).first()

    if not the_document or not the_episode:
        raise HTTPException(404, "document or episode not found!")

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
        raise HTTPException(500, "unable to delete the episode completely!")
    else:
        db.delete(the_episode)
        db.commit()
        return ResponseMessage(error=False, message="episode deleted")
