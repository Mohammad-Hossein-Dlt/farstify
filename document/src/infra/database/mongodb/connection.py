from pymongo.asynchronous.database import AsyncDatabase
from beanie import init_beanie
from pymongo.asynchronous.mongo_client import AsyncMongoClient

from .collections.document.document_collection import DocumentCollection
from .collections.document.document_image_collection import DocumentImageCollection
from .collections.document.document_link_collection import DocumentLinkCollection

from .collections.episode.episode_collection import EpisodeCollection
from .collections.episode.episode_image_collection import EpisodeImageCollection
from .collections.episode.episode_link_collection import EpisodeLinkCollection



async def init_mongodb_client(
    host: str,
    port: int,
    username: str,
    password: str,
    db_name: str
) -> AsyncMongoClient:
    
    client = AsyncMongoClient(
        host=host,
        port=port,
        username=username,
        password=password,
    )
    
    database = AsyncDatabase(
        client=client,
        name=db_name,
    )
    
    await init_beanie(
        database=database,
        document_models=[
            DocumentCollection,
            DocumentImageCollection,
            DocumentLinkCollection,
            
            EpisodeCollection,
            EpisodeImageCollection,
            EpisodeLinkCollection
        ],
    )
    
    return client