from fastapi import Depends
from sqlalchemy.orm import Session
from pymongo.asynchronous.mongo_client import AsyncMongoClient
from .db_depend import db_client_depend

from src.repo.interface.user.Iuser_repo import IUserRepo
from src.repo.mongodb.user.user_repo import UserMongodbRepo
   
from src.repo.interface.user.Iuser_image_repo import IUserImageRepo
from src.repo.mongodb.user.user_image_repo import UserImageMongodbRepo
   
from src.repo.interface.user.Iuser_link_repo import IUserLinkRepo
from src.repo.mongodb.user.user_link_repo import UserLinkMongodbRepo

from src.repo.interface.follow.Ifollows_repo import IFollowsRepo
from src.repo.mongodb.follow.follows_repo import FollowsMongodbRepo

from src.repo.interface.like.Ilikes_repo import ILikesRepo
from src.repo.mongodb.like.likes_repo import LikeMongodbRepo
   
def user_repo_depend(
    db_client: AsyncMongoClient | Session = Depends(db_client_depend)
) -> IUserRepo:

    if isinstance(db_client, AsyncMongoClient):
        return UserMongodbRepo()
   
def user_image_repo_depend(
    db_client: AsyncMongoClient | Session = Depends(db_client_depend)
) -> IUserImageRepo:

    if isinstance(db_client, AsyncMongoClient):
        return UserImageMongodbRepo()
    
def user_link_repo_depend(
    db_client: AsyncMongoClient | Session = Depends(db_client_depend)
) -> IUserLinkRepo:

    if isinstance(db_client, AsyncMongoClient):
        return UserLinkMongodbRepo()

def follow_repo_depend(
    db_client: AsyncMongoClient | Session = Depends(db_client_depend)
) -> IFollowsRepo:

    if isinstance(db_client, AsyncMongoClient):
        return FollowsMongodbRepo()
    
def like_repo_depend(
    db_client: AsyncMongoClient | Session = Depends(db_client_depend)
) -> ILikesRepo:

    if isinstance(db_client, AsyncMongoClient):
        return LikeMongodbRepo()