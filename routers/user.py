import models
import uuid
import pathlib
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from access_token import create_access_token, token_dependency, user_token_dependency
from storage import storage, Buckets, storage_delete_file
from db_dependency import db_dependency
from fastapi import APIRouter, HTTPException, status, UploadFile, File, Depends
from pydantic import BaseModel
from actions.response_model import ResponseMessage
from typing import Annotated, List
from sqlalchemy import and_, or_, asc, desc
from utills.path_manager import make_path
from utills.check_username import uniq_user_name, check_username
from constants import AccountTypes, OrderBy, ContentTypes
from actions.user_actions import user_profile_data
from actions.artist_short_info_actions import get_artist_short_info
from actions.document_actions import get_document_short_info
from actions.episode_actions import get_episode_short_info
from actions.playlist_actions import get_playlist_short_info, get_playlist_full_info

router = APIRouter(prefix="/user", tags=["User"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SignUp(BaseModel):
    Name: str
    Phone: str
    Password: str
    Email: str | None = None
    VerifyCode: str


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/profile", status_code=status.HTTP_201_CREATED)
async def verify_user(
        db: db_dependency,
        access_token: token_dependency,
):
    user = db.query(models.Users).where(models.Users.UserName == access_token.user_name).first()

    if not user:
        raise HTTPException(404, "an error occurred!")

    return await user_profile_data(user)


@router.post("/sign-up", status_code=status.HTTP_201_CREATED)
async def sign_up_action(
        db: db_dependency,
        sign_up: SignUp,
):
    check = db.query(models.Users).where(models.Users.Phone == sign_up.Phone).first()

    verify_code = db.query(models.UsersTemp).where(
        and_(
            models.UsersTemp.Phone == sign_up.Phone,
            models.UsersTemp.VerifyCode == sign_up.VerifyCode
        )

    ).first()

    verify_code = True

    if check:
        raise HTTPException(201, "user already signed up!")

    if verify_code is None:
        raise HTTPException(403, "you are not verified")

    user = models.Users()
    user.Name = sign_up.Name.strip()
    user.Phone = sign_up.Phone.strip()
    user.Password = pwd_context.hash(sign_up.Password.strip())
    user.Email = sign_up.Email.strip() if sign_up.Email else None
    db.add(user)

    db.commit()

    path = make_path(user.DirectoryName, is_file=False)
    storage.put_object(Bucket=Buckets.USER_BUCKET_NAME, Key=path)

    return ResponseMessage(error=False, message="User has been signed up!")


@router.post("/sign-in", status_code=status.HTTP_201_CREATED)
async def sign_in(
        db: db_dependency,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    check = db.query(models.Users).where(
        or_(
            models.Users.Phone == form_data.username,
            models.Users.UserName == form_data.username,
        )
    ).first()

    verify_code = db.query(models.UsersTemp).where(
        and_(
            models.UsersTemp.Phone == form_data.username,
        )

    ).first()

    if check is None:
        raise HTTPException(403, "You are not signed up")

    password_check = pwd_context.verify(form_data.password, check.Password)

    verify_code_check = verify_code.VerifyCode == form_data.password if verify_code else False

    if password_check or verify_code_check:
        to_encode = {"username": check.UserName, "id": check.Id, "type": AccountTypes.user}
        access_token = create_access_token(to_encode)
        return Token(access_token=access_token, token_type="bearer")

    if not password_check or not verify_code:
        raise HTTPException(403, "Incorrect password or verified")


@router.post("/change-profile-image", status_code=status.HTTP_201_CREATED)
async def change_profile_image(
        db: db_dependency,
        access_token: user_token_dependency,
        image_file: UploadFile = File(None),
        delete_image: bool = False,
):
    user = db.query(models.Users).where(models.Users.Id == access_token.user_id).first()

    main_path = make_path(user.DirectoryName, is_file=False)

    def delete_image_action(image: str):
        try:
            delete_previous = make_path(main_path, image, is_file=True)
            storage_delete_file(delete_previous, Buckets.USER_BUCKET_NAME)
        except Exception as ex:
            print(ex)

    if image_file and not delete_image:
        file_name = uuid.uuid4().hex + pathlib.Path(image_file.filename).suffix
        image_path = make_path(main_path, file_name, is_file=True)
        try:
            storage.upload_fileobj(image_file.file, Bucket=Buckets.USER_BUCKET_NAME, Key=image_path)
        except Exception as ex:
            print(ex)
        else:
            delete_image_action(user.ProfileImage)
            user.ProfileImage = file_name
            db.commit()
    elif not image_file and delete_image:
        delete_image_action(user.ProfileImage)
        user.ProfileImage = None
        db.commit()

    return ResponseMessage(error=False, message="User profile image has been changed!")


@router.put("/edit-profile", status_code=status.HTTP_201_CREATED)
async def edit_profile(
        db: db_dependency,
        access_token: user_token_dependency,
        name: str | None = None,
        email: str | None = None,
):
    user = db.query(models.Users).where(models.Users.Id == access_token.user_id).first()
    user.Name = name.strip() if name else user.Name
    user.Email = email.strip() if email else user.Email

    db.commit()
    return ResponseMessage(error=False, message="User profile has been changed!")


@router.put("/change-username", status_code=status.HTTP_201_CREATED)
async def change_username(
        db: db_dependency,
        access_token: user_token_dependency,
        username: str,
):
    username = username.strip()

    user = db.query(models.Users).where(models.Users.Id == access_token.user_id).first()

    if user and check_username(username=username):
        if await uniq_user_name(db, username):
            user.UserName = username
            db.commit()
            return ResponseMessage(error=False, message="User-name has been changed!")
        else:
            raise HTTPException(403, f"the username {username} is not available")


@router.put("/change-password", status_code=status.HTTP_201_CREATED)
async def change_password(
        db: db_dependency,
        access_token: user_token_dependency,
        password: str,
        newpassword: str,
):
    user = db.query(models.Users).where(models.Users.Id == access_token.user_id).first()
    if user is None:
        raise HTTPException(403, "You are not signed up")
    verify_code = db.query(models.UsersTemp).where(
        and_(
            models.UsersTemp.Phone == user.Phone,
            models.UsersTemp.VerifyCode == password
        )

    ).first()
    if user and (pwd_context.verify(password, user.Password) or verify_code):
        user.Password = pwd_context.hash(newpassword.strip())
        db.commit()
        return ResponseMessage(error=False, message="User password has been changed!")
    elif user is None:
        raise HTTPException(403, "You are not signed up")
    elif user and not pwd_context.verify(password, user.Password):
        raise HTTPException(403, "Incorrect password")
    elif verify_code is None:
        raise HTTPException(403, "You are not verified")


@router.put("/change-phone", status_code=status.HTTP_201_CREATED)
async def change_phone(
        db: db_dependency,
        access_token: user_token_dependency,
        new_phone: str,
        verifycode: str,
):
    new_phone = new_phone.strip()

    new_phone_exists = db.query(models.Users).where(models.Users.Phone == new_phone).first()

    user = db.query(models.Users).where(models.Users.Id == access_token.user_id).first()
    if not user:
        raise HTTPException(403, "You are not signed up")

    verify_code = db.query(models.UsersTemp).where(
        and_(
            models.UsersTemp.Phone == new_phone,
            models.UsersTemp.VerifyCode == verifycode
        )

    ).first()

    if new_phone_exists is None and verify_code:
        user.Phone = new_phone
        db.commit()
        return ResponseMessage(error=False, message="User phone has been changed!")
    elif new_phone_exists:
        raise HTTPException(403, "Your new phone already exists")
    elif not verify_code:
        raise HTTPException(403, "Your new phone not verified")


@router.post("/create-playlist", status_code=status.HTTP_201_CREATED)
async def create_playlist(
        db: db_dependency,
        access_token: user_token_dependency,
        title: str | None,
        public: bool = False,
):

    new_play_list = models.PlayList()

    new_play_list.OwnerUser = access_token.user_id

    new_play_list.Title = title

    new_play_list.Public = public

    db.add(new_play_list)
    db.commit()

    return ResponseMessage(error=False, message="Playlist has been created!")


@router.post("/edit-playlist", status_code=status.HTTP_201_CREATED)
async def edit_playlist(
        db: db_dependency,
        access_token: user_token_dependency,
        play_list_id: int,
        title: str
):
    the_play_list = db.query(models.PlayList).where(
        and_(
            models.PlayList.Id == play_list_id,
            models.PlayList.OwnerUser == access_token.user_id
        )
    ).first()

    if the_play_list:
        the_play_list.Title = title
        db.commit()

    return ResponseMessage(error=False, message="Playlist has been updated!")


@router.put("/reorder_playlist", status_code=status.HTTP_200_OK)
async def reorder_contributors(
        db: db_dependency,
        access_token: user_token_dependency,
        play_list_id: int,
        episodes_id: List[int],
):
    the_play_list = db.query(models.PlayList).where(
        and_(
            models.PlayList.Id == play_list_id,
            models.PlayList.OwnerUser == access_token.user_id
        )
    ).first()
    if the_play_list:
        for i in episodes_id:
            check = db.query(models.PlayListRepository).where(
                and_(
                    models.PlayListRepository.EpisodesId == i,
                    models.PlayListRepository.PlayListId == the_play_list.Id,
                )
            ).first()
            if check:
                check.OrderBy = episodes_id.index(i)
                db.commit()

    return ResponseMessage(error=False, message="Contributors has been reordered!")


@router.delete("/delete-playlist", status_code=status.HTTP_201_CREATED)
async def delete_playlist(
        db: db_dependency,
        access_token: user_token_dependency,
        play_list_id: int,
):
    the_play_list = db.query(models.PlayList).where(
        and_(
            models.PlayList.Id == play_list_id,
            models.PlayList.OwnerUser == access_token.user_id,
        )
    ).first()

    if the_play_list:
        db.delete(the_play_list)
        db.commit()

    return ResponseMessage(error=False, message="Playlist has been deleted!")


@router.post("/add-to-playlist", status_code=status.HTTP_201_CREATED)
async def add_to_playlist(
        db: db_dependency,
        access_token: user_token_dependency,
        episode_id: int,
        play_list_id: int,
):
    the_play_list = db.query(models.PlayList).where(
        and_(
            models.PlayList.Id == play_list_id,
            models.PlayList.OwnerUser == access_token.user_id,
        )
    ).first()

    episode_data = db.query(models.DocumentsEpisodes).where(
        models.DocumentsEpisodes.Id == episode_id
    ).first()

    if not episode_data:
        raise HTTPException(403, "No episode exist.")
    if the_play_list:

        item = db.query(models.PlayListRepository).where(
            and_(
                models.PlayListRepository.PlayListId == the_play_list.Id,
                models.PlayListRepository.EpisodesId == episode_id,
            )
        ).first()

        if not item:
            playlist_episode = models.PlayListRepository()
            playlist_episode.PlayListId = the_play_list.Id
            playlist_episode.DocumentId = episode_data.DocumentId
            playlist_episode.EpisodesId = episode_data.Id
            db.add(playlist_episode)
            db.commit()
            return ResponseMessage(error=False, message="Episode has been added to playlist!")
        else:
            db.delete(item)
            db.commit()
            return ResponseMessage(error=False, message="Episode has been deleted from playlist!")


@router.get("/fetch-all-playlists", status_code=status.HTTP_201_CREATED)
async def fetch_all_playlists(
        db: db_dependency,
        access_token: user_token_dependency,
        limit: int,
        page: int,
):
    pl = []
    play_lists = db.query(models.PlayList).where(
        models.PlayList.OwnerUser == access_token.user_id
    ).limit(limit).offset(limit * page).all()

    if play_lists.__contains__(None):
        play_lists = []

    for i in play_lists:
        pl.append(await get_playlist_short_info(db=db, playlist=i))
        # first_ep = db.query(models.DocumentsEpisodes).select_from(models.PlayListRepository).where(
        #     models.PlayListRepository.PlayListId == i.Id
        # ).first()
        # document = db.query(models.Document).where(models.Document.Id == first_ep.DocumentId).first()
        # i.directory = document.DirectoryName
        # i.Image = first_ep.Image if first_ep.Image is not None else document.MainImage

    return pl


@router.get("/fetch-playlist_episodes", status_code=status.HTTP_201_CREATED)
async def fetch_playlist_episodes(
        db: db_dependency,
        play_list_id: int,
        order_by: OrderBy,
):

    result = []

    episodes = db.query(models.PlayListRepository, models.DocumentsEpisodes, models.Document).join(
        models.DocumentsEpisodes,
        models.PlayListRepository.EpisodesId == models.DocumentsEpisodes.Id,
        isouter=True
    ).join(
        models.Document,
        models.PlayListRepository.DocumentId == models.Document.Id,
        isouter=True
    ).where(
        models.PlayListRepository.PlayListId == play_list_id,
    ).order_by(
        desc(models.PlayListRepository.Id) if order_by is OrderBy.desc else asc(models.PlayListRepository.Id)
    ).all()

    if not episodes and episodes.__contains__(None):
        episodes = []

    for _, episode, document in episodes:
        result.append(await get_episode_short_info(db=db, episode=episode, document=document))

    return result


@router.put("/like-episode", status_code=status.HTTP_201_CREATED)
async def like_episode(
        db: db_dependency,
        access_token: user_token_dependency,
        episode_id: int,
):
    episode, document = db.query(models.DocumentsEpisodes, models.Document).join(
        models.Document
    ).where(
        models.DocumentsEpisodes.Id == episode_id
    ).first()

    # like = like_episode_mongo(
    #     History(
    #         userId=accessToken.id_,
    #         artistId=document.Owner,
    #         documentId=episode.DocumentId,
    #         episodeId=episode.Id,
    #         contentType=document.ContentType
    #     )
    # )
    #
    # if like:
    #     return ResponseMessage(error=False, message="Ok. you liked this content.")
    # else:
    #     return ResponseMessage(error=False, message="Ok. your like has been removed.")

    check = db.query(models.UserLikes).where(
        and_(
            models.UserLikes.UserId == access_token.user_id,
            models.UserLikes.DocumentId == episode.DocumentId,
            models.UserLikes.EpisodeId == episode_id,
        )
    ).first()

    if not check:
        like = models.UserLikes(UserId=access_token.user_id, DocumentId=episode.DocumentId, EpisodeId=episode.Id)
        db.add(like)
        db.commit()
        return ResponseMessage(error=False, message="Ok. you liked this content.")
    else:
        db.delete(check)
        db.commit()
        return ResponseMessage(error=False, message="Ok. your like has been removed.")


@router.get("/fetch-likes", status_code=status.HTTP_200_OK)
async def fetch_likes(
        db: db_dependency,
        access_token: user_token_dependency,
        limit: int, page: int,
        order_by: OrderBy,
        content_types: ContentTypes,
):
    result = []
    #
    # ids = get_likes_by_type(userId=accessToken.id_, contentType=contentType, limit=limit, page=page, order=orderBy)
    #
    # order_case = case({id_: index for index, id_ in enumerate(ids)}, value=models.DocumentsEpisodes.Id)
    #
    # likes = db.query(models.DocumentsEpisodes, models.Document).join(
    #     models.Document
    # ).where(
    #     models.DocumentsEpisodes.Id.in_(ids),
    # ).order_by(
    #     order_case,
    # ).all()
    #
    # if not likes or likes.__contains__(None):
    #     return []
    #
    # for i in likes:
    #     result.append(await episode_data(db=db, episode=i[0], document=i[1]))

    # docs = db.query(models.DocumentsEpisodes, models.Document).select_from(models.UserLikes).filter(
    #     and_(
    #         models.UserLikes.UserId == accessToken.id_,
    #         models.Document.ContentType == contentType,
    #     )
    # ).order_by(
    #     desc(models.UserLikes.Id) if orderBy is OrderBy.desc else asc(models.UserLikes.Id)
    # ).limit(limit).offset(limit * page).all()

    docs = db.query(models.UserLikes, models.DocumentsEpisodes, models.Document).select_from(models.UserLikes).join(
        models.DocumentsEpisodes,
    ).join(
        models.Document,
    ).filter(
        models.UserLikes.UserId == access_token.user_id,
        models.Document.ContentType == content_types,
    ).order_by(
        desc(models.UserLikes.Id) if order_by is OrderBy.desc else asc(models.UserLikes.Id)
    ).limit(limit).offset(limit * page).all()

    for _, episode, document in docs:
        result.append(await get_episode_short_info(db=db, episode=episode, document=document))

    return result


@router.put("/follow", status_code=status.HTTP_200_OK)
async def follow(
        db: db_dependency,
        access_token: user_token_dependency,
        artist_id: int | None = None,
        document_id: int | None = None,
        play_list_id: int | None = None,
):
    params = [artist_id, document_id, play_list_id]

    given_params_num = sum(p is not None for p in params)

    if given_params_num != 1:
        raise HTTPException(403, "only one entity must be given")

    check = db.query(models.UserFollowing).where(
        and_(
            models.UserFollowing.ArtistId == artist_id,
            models.UserFollowing.DocumentId == document_id,
            models.UserFollowing.PlayListId == play_list_id,
        ),
    ).first()

    if check:
        db.delete(check)
        db.commit()
        return ResponseMessage(error=False, message="Ok. your following has been removed.")

    new_follow = models.UserFollowing()
    new_follow.UserId = access_token.user_id

    if artist_id:
        new_follow.ArtistId = artist_id

    if document_id:
        new_follow.DocumentId = document_id

    if play_list_id:
        new_follow.PlayListId = play_list_id

    db.add(new_follow)
    db.commit()

    return ResponseMessage(error=False, message="Ok. your following has added.")


@router.get("/fetch_following", status_code=status.HTTP_200_OK)
async def fetch_following(
        db: db_dependency,
        access_token: user_token_dependency,
        limit: int,
        page: int,
        order_by: OrderBy,
):
    result = []

    docs = db.query(models.UserFollowing, models.Artists, models.Document, models.PlayList).join(
        models.Artists,
        models.UserFollowing.ArtistId == models.Artists.Id,
        isouter=True,
    ).join(
        models.Document,
        models.UserFollowing.DocumentId == models.Document.Id,
        isouter=True,
    ).join(
        models.PlayList,
        models.UserFollowing.PlayListId == models.PlayList.Id,
        isouter=True,
    ).filter(
        models.UserFollowing.UserId == access_token.user_id
    ).order_by(
        desc(models.UserFollowing.Id) if order_by is OrderBy.desc else asc(models.UserFollowing.Id)
    ).limit(limit).offset(limit * page).all()

    for _, artist, document, playlist in docs:
        if artist:
            result.append({"type": "artist", "data": get_artist_short_info(artist)})

        if document:
            result.append({"type": "document", "data": await get_document_short_info(db=db, document=document)})

        if playlist:
            result.append({"type": "playlistId", "data": await get_playlist_short_info(db, playlist)})

    return result

# @router.put("/follow", status_code=status.HTTP_200_OK)
# async def follow(
#         db: db_dependency,
#         accessToken: token_dependency,
#         follow_entity_type: FollowEntities,
#         follow_id: int
# ):
#     new_following = add_following(
#         follow_action=FollowAction(
#             userId=accessToken.id_,
#             follow_entity_type=follow_entity_type,
#             follow_id=follow_id,
#         ),
#     )
#
#     if new_following:
#         return ResponseMessage(error=False, message="your following has been added.")
#     else:
#         return ResponseMessage(error=False, message="Ok. your following has been removed.")

#
# @router.get("/fetch_following", status_code=status.HTTP_200_OK)
# async def fetch_following(
#         db: db_dependency,
#         accessToken: token_dependency,
#         limit: int,
#         page: int,
#         orderBy: OrderBy,
# ):
#     result = []
#     ids = get_following(userId=accessToken.id_, page=page, limit=limit)
#
#     for follow_item in ids:
#         if follow_item.follow_entity_type == FollowEntities.artist:
#             artist = db.query(models.Artists).where(models.Artists.Id == follow_item.follow_id).first()
#             result.append({"type": "artist", "data": await simple_artist_profile_data(artist)})
#
#         if follow_item.follow_entity_type == FollowEntities.document:
#             document = db.query(models.Document).where(models.Document.Id == follow_item.follow_id).first()
#             result.append({"type": "document", "data": await document_data(db=db, document=document, onList=True)})
#
#         if follow_item.follow_entity_type == FollowEntities.playlist:
#             playlist = db.query(models.PlayList).where(models.PlayList.Id == follow_item.follow_id).first()
#             result.append({"type": "playlist", "data": await playlist_data(db=db, playlist=playlist)})
#
#     return result
