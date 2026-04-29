from fastapi import Depends
from sqlalchemy.orm import Session
from pymongo.asynchronous.mongo_client import AsyncMongoClient
from .db_depend import db_client_depend

from src.repo.interface.Iartist_repo import IArtistRepo
from src.repo.mongodb.artist_repo import ArtistMongodbRepo
   
from src.repo.interface.Iartist_image_repo import IArtistImageRepo
from src.repo.mongodb.artist_image_repo import ArtistImageMongodbRepo
   
from src.repo.interface.Iartist_link_repo import IArtistLinkRepo
from src.repo.mongodb.artist_link_repo import ArtistLinkMongodbRepo
   
def artist_repo_depend(
    db_client: AsyncMongoClient | Session = Depends(db_client_depend)
) -> IArtistRepo:
    
    # if isinstance(db_client, Session):
    #     return ArtistsMongodbRepo(db_client)
    
    if isinstance(db_client, AsyncMongoClient):
        return ArtistMongodbRepo()
   
def artist_image_repo_depend(
    db_client: AsyncMongoClient | Session = Depends(db_client_depend)
) -> IArtistImageRepo:
    
    # if isinstance(db_client, Session):
    #     return ArtistsMongodbRepo(db_client)
    
    if isinstance(db_client, AsyncMongoClient):
        return ArtistImageMongodbRepo()
    
def artist_link_repo_depend(
    db_client: AsyncMongoClient | Session = Depends(db_client_depend)
) -> IArtistLinkRepo:
    
    # if isinstance(db_client, Session):
    #     return ArtistsMongodbRepo(db_client)
    
    if isinstance(db_client, AsyncMongoClient):
        return ArtistLinkMongodbRepo()
