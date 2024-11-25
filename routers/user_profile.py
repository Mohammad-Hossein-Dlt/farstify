import models
from fastapi import APIRouter, HTTPException, status
from db_dependency import db_dependency
from actions.user_actions import user_profile_data

router = APIRouter(prefix="/user_profile", tags=["User-Profile"])


@router.get("/personal", status_code=status.HTTP_201_CREATED)
async def verify_user(
        db: db_dependency,
        username: str,
):
    user = db.query(models.Users).where(models.Users.UserName == username).first()

    if not user:
        raise HTTPException(404, "an error occurred!")

    return await user_profile_data(user)


@router.get("/playlists", status_code=status.HTTP_201_CREATED)
async def fetch_all_playlists(
        db: db_dependency,
        username: str,
        limit: int,
        page: int,
):
    user = db.query(models.Users).where(models.Users.UserName == username).first()

    if not user:
        raise HTTPException(404, "an error occurred!")

    play_lists = db.query(models.PlayList).where(
        models.PlayList.OwnerUser == user.Id
    ).limit(limit).offset(limit * page).all()

    if play_lists.__contains__(None):
        play_lists = []

    for i in play_lists:
        first_ep = db.query(models.DocumentsEpisodes).select_from(models.PlayListRepository).where(
            models.PlayListRepository.PlayListId == i.Id
        ).first()
        document = db.query(models.Document).where(models.Document.Id == first_ep.DocumentId).first()
        i.directory = document.DirectoryName
        i.Image = first_ep.Image if first_ep.Image is not None else document.MainImage

    return play_lists
