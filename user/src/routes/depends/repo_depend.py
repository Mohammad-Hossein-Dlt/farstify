from fastapi import Depends
from sqlalchemy.orm import Session
from pymongo.asynchronous.mongo_client import AsyncMongoClient
from .db_depend import db_client_depend

from src.repo.interface.Iuser_repo import IUserRepo
from src.repo.mongodb.user_repo import UserMongodbRepo
   
from src.repo.interface.Iuser_image_repo import IUserImageRepo
from src.repo.mongodb.user_image_repo import UserImageMongodbRepo
   
from src.repo.interface.Iuser_link_repo import IUserLinkRepo
from src.repo.mongodb.user_link_repo import UserLinkMongodbRepo
   
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
