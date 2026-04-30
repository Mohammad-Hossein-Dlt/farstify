from fastapi import Depends
from sqlalchemy.orm import Session
from pymongo.asynchronous.mongo_client import AsyncMongoClient
from .db_depend import db_client_depend

from src.repo.interface.document.Idocument_repo import IDocumentRepo
from src.repo.mongodb.document.document_repo import DocumentMongodbRepo
   
from src.repo.interface.document.Idocument_image_repo import IDocumentImageRepo
from src.repo.mongodb.document.document_image_repo import DocumentImageMongodbRepo
   
from src.repo.interface.document.Idocument_link_repo import IDocumentLinkRepo
from src.repo.mongodb.document.document_link_repo import DocumentLinkMongodbRepo

from src.repo.interface.episode.Iepisode_repo import IEpisodeRepo
from src.repo.mongodb.episode.episode_repo import EpisodeMongodbRepo
   
from src.repo.interface.episode.Iepisode_image_repo import IEpisodeImageRepo
from src.repo.mongodb.episode.episode_image_repo import EpisodeImageMongodbRepo
   
from src.repo.interface.episode.Iepisode_link_repo import IEpisodeLinkRepo
from src.repo.mongodb.episode.episode_link_repo import EpisodeLinkMongodbRepo
   
def document_repo_depend(
    db_client: AsyncMongoClient | Session = Depends(db_client_depend)
) -> IDocumentRepo:
    
    if isinstance(db_client, AsyncMongoClient):
        return DocumentMongodbRepo()
   
def document_image_repo_depend(
    db_client: AsyncMongoClient | Session = Depends(db_client_depend)
) -> IDocumentImageRepo:
    
    if isinstance(db_client, AsyncMongoClient):
        return DocumentImageMongodbRepo()
    
def document_link_repo_depend(
    db_client: AsyncMongoClient | Session = Depends(db_client_depend)
) -> IDocumentLinkRepo:
    
    if isinstance(db_client, AsyncMongoClient):
        return DocumentLinkMongodbRepo()
   
def episode_repo_depend(
    db_client: AsyncMongoClient | Session = Depends(db_client_depend)
) -> IEpisodeRepo:
    
    if isinstance(db_client, AsyncMongoClient):
        return EpisodeMongodbRepo()
   
def episode_image_repo_depend(
    db_client: AsyncMongoClient | Session = Depends(db_client_depend)
) -> IEpisodeImageRepo:
    
    if isinstance(db_client, AsyncMongoClient):
        return EpisodeImageMongodbRepo()
    
def episode_link_repo_depend(
    db_client: AsyncMongoClient | Session = Depends(db_client_depend)
) -> IEpisodeLinkRepo:
    
    if isinstance(db_client, AsyncMongoClient):
        return EpisodeLinkMongodbRepo()
