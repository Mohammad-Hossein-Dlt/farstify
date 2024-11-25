import models
import os
from access_token import decode_access_token
from fastapi import APIRouter, status, HTTPException
from fastapi.responses import StreamingResponse
from io import BytesIO

from actions_functions.listened import add_listened
from storage import storage, Buckets
from db_dependency import db_dependency
from constants import DocumentQualities
from utills.path_manager import make_path
from utills.encode_link import decode_link

router = APIRouter()


@router.get("/file/{url}", status_code=status.HTTP_200_OK, tags=["File Url"])
async def document_file(
        url: str,
):
    try:
        decoded_url = decode_link(url)
        response = storage.get_object(Bucket=decoded_url.bucket, Key=decoded_url.path)
        file = response["Body"].read()
        content_type = response["ContentType"]
        print(content_type)

        b = BytesIO()
        b.write(file)
        b.seek(0)
        return StreamingResponse(b,  headers={"Content-Disposition": "inline"})
    except Exception as ex:
        raise HTTPException(404, "url not exist or an error occurred!")


@router.get("/play-audio", status_code=status.HTTP_200_OK, tags=["File Url"])
async def document_file2(
        db: db_dependency,
        episode_id: int,
        quality: str | None = None,
        _token_: str | None = None,
):
    token = decode_access_token(encoded_token=_token_, empty_data=True) if _token_ else None

    episode, document = db.query(models.DocumentsEpisodes, models.Document).join(
        models.Document
    ).where(
        models.DocumentsEpisodes.Id == episode_id
    ).first()

    def qualify_validator():
        if quality:
            check_value = quality.replace("k", "")
            if quality.isalnum() and check_value.isnumeric() and 24 <= int(check_value) <= 320:
                return True
            else:
                return False

    is_valid_qualify = qualify_validator()

    def check_pre_converted():
        if is_valid_qualify:
            return True if DocumentQualities.directories().__contains__(quality) else False
        else:
            return False

    is_pre_converted = check_pre_converted()

    path = make_path(document.DirectoryName, DocumentQualities.q128k_bit if token else DocumentQualities.preview,
                     episode.File, is_file=True)

    if token.permission and token.account_type == "user":
        await add_listened(
            db=db,
            artist_id=document.Owner,
            user_id=token.user_id,
            document_id=document.Id,
            episode_id=episode.Id,
        )

    headers = {
        # "Content-Disposition": f"filename={episode.File}",
        "Content-Disposition": "inline",
        "Content-Type": "audio/mpeg",
        "Accept-Ranges": "bytes",
        "Content-Length": "",
    }

    if not token:
        path = make_path(document.DirectoryName, DocumentQualities.preview, episode.File, is_file=True)
        response = storage.get_object(Bucket=Buckets.DOCUMENT_BUCKET_NAME, Key=path)
        headers.update(
            {
                "Content-Length": str(response["ContentLength"])
            }
        )
        audio = response["Body"]
        print(response["ContentLength"])

        return StreamingResponse(audio, headers=headers)

    elif is_pre_converted:
        path = make_path(document.DirectoryName, quality, episode.File, is_file=True)
        response = storage.get_object(Bucket=Buckets.DOCUMENT_BUCKET_NAME, Key=path)
        headers.update(
            {
                "Content-Length": str(response["ContentLength"])
            }
        )
        audio = response["Body"]

        return StreamingResponse(audio, headers=headers)
    else:

        if is_valid_qualify:
            pass
            # path = make_path(document.DirectoryName, episode.File, is_file=True)
            #
            # audio = AudioSegment.from_file(path)
            #
            # modified = AudioSegment(
            #     audio.get_array_of_samples(),
            #     frame_rate=audio.frame_rate,
            #     sample_width=audio.sample_width,
            #     channels=audio.channels,
            # )
            #
            # stream = BytesIO()
            # modified.export(stream, bitrate=quality)
            #
            # stream.seek(0)
            # data = stream.getvalue()
            #
            # print(len(data))
            #
            # headers.update(
            #     {
            #         "Content-Length": str(len(data))
            #     }
            # )
            # return StreamingResponse(iter([data]), headers=headers)

        else:

            headers.update(
                {
                    "Content-Length": str(os.path.getsize(path))
                }
            )

            def stream_():
                with open(path, 'rb') as audio_:
                    while True:
                        chunk = audio_.read(1024)
                        if not chunk:
                            break
                        yield chunk

            return StreamingResponse(stream_(), headers=headers)
