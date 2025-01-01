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
from utills.parse_null import pars_null
from utills.path_manager import make_path
from utills.encode_link import decode_link

router = APIRouter(prefix="/media", tags=["Media"])


@router.get("/file/{url}", status_code=status.HTTP_200_OK)
async def document_file(
        url: str,
):
    try:
        decoded_url = decode_link(url)
        response = storage.get_object(Bucket=decoded_url.bucket, Key=decoded_url.path)
        file = response["Body"].read()
        # content_type = response["ContentType"]
        # print(content_type)
        b = BytesIO()
        b.write(file)
        b.seek(0)
        return StreamingResponse(b, headers={"Content-Disposition": "inline"})
    except Exception as ex:
        raise HTTPException(404, "url not exist or an error occurred!")


@router.get("/play_audio", status_code=status.HTTP_200_OK)
async def document_file2(
        db: db_dependency,
        episode_id: int,
        quality: str | None = None,
        token_value: str | None = None,
        # admin_access: bool = False,
):
    quality = pars_null(quality)
    token_value = pars_null(token_value)

    token = decode_access_token(encoded_token=token_value, empty_data=True) if token_value else None

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

    def check_pre_converted():
        if qualify_validator():
            return True if DocumentQualities.directories().__contains__(quality) else False
        else:
            return False

    if token and token.permission and token.account_type == "user":
        add_listened(
            db=db,
            user_id=token.user_id,
            episode_id=episode.Id,
        )

    headers = {
        "Content-Disposition": "inline",
        "Content-Type": "audio/mpeg",
        "Accept-Ranges": "bytes",
        "Content-Length": "",
    }

    def play(folder: str):
        path = make_path(document.DirectoryName, folder, episode.File, is_file=True)
        response = storage.get_object(Bucket=Buckets.DOCUMENT_BUCKET_NAME, Key=path)
        headers.update(
            {
                "Content-Length": str(response["ContentLength"])
            }
        )
        audio = response["Body"]
        return StreamingResponse(audio, headers=headers)

    # if not token and not admin_access:
    #     return play(DocumentQualities.preview)
    if check_pre_converted():
        return play(quality)
    else:
        return play(DocumentQualities.q128k_bit)


