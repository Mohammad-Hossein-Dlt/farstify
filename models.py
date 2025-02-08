import uuid
from sqlalchemy import ForeignKey, Column, Text, Numeric, Boolean, Enum, Integer, BigInteger, DateTime, func
from database import *
from constants import *


class Task(Base):
    __tablename__ = 'Task'
    Id = Column(BigInteger, primary_key=True, autoincrement=True)
    EpisodeId = Column(ForeignKey("DocumentsEpisodes.Id", ondelete="CASCADE"), nullable=False)
    ActionState = Column(Enum(ProcessActionTaskState), nullable=False)
    CreationDate = Column(DateTime, nullable=False, server_default=func.now())


class Document(Base):
    __tablename__ = 'Document'
    Id = Column(BigInteger, primary_key=True, autoincrement=True)
    DirectoryName = Column(Text, unique=True, nullable=False, default=lambda: uuid.uuid4().hex)
    Name = Column(Text, nullable=False)
    MainImage = Column(Text, nullable=True)
    Color = Column(Text, nullable=True)
    Description = Column(Text, nullable=True)
    ContentType = Column(Enum(ContentTypes), nullable=False)
    Single = Column(Boolean(), nullable=False, default=True)
    Active = Column(Boolean(), nullable=False, default=True)
    CreationDate = Column(Text, nullable=False, server_default=func.now())


class DocumentsCategories(Base):
    __tablename__ = 'DocumentsCategories'
    Id = Column(BigInteger, primary_key=True, autoincrement=True)
    DocumentId = Column(ForeignKey("Document.Id", ondelete="CASCADE"), nullable=False)
    CategoryId = Column(ForeignKey("Categories.Id", ondelete="CASCADE"), nullable=False)
    OrderBy = Column(Integer, nullable=True)
    CreationDate = Column(Text, nullable=False, server_default=func.now())


class DocumentsEpisodes(Base):
    __tablename__ = 'DocumentsEpisodes'
    Id = Column(BigInteger, primary_key=True, autoincrement=True)
    DocumentId = Column(ForeignKey("Document.Id", ondelete="CASCADE"), nullable=False)
    Title = Column(Text, nullable=False)
    Image = Column(Text, nullable=True)
    File = Column(Text, nullable=True)
    Duration = Column(BigInteger, nullable=False, default=0)
    OrderBy = Column(Integer, nullable=True)
    CreationDate = Column(Text, nullable=False, server_default=func.now())


class ListenedHistory(Base):
    __tablename__ = 'ListenedHistory'
    Id = Column(Numeric(precision=100, scale=0), primary_key=True, unique=True)
    UserId = Column(ForeignKey("Users.Id", ondelete="CASCADE"), nullable=False)
    EpisodeId = Column(ForeignKey("DocumentsEpisodes.Id", ondelete="CASCADE"), nullable=False)
    CreationDate = Column(Text, nullable=False, server_default=func.now())


class DocumentsOwners(Base):
    __tablename__ = 'DocumentsOwners'
    Id = Column(BigInteger, primary_key=True, autoincrement=True)
    ArtistId = Column(ForeignKey("Artists.Id", ondelete="CASCADE"), nullable=False)
    DocumentId = Column(ForeignKey("Document.Id", ondelete="CASCADE"), nullable=False)
    OrderBy = Column(Integer, nullable=True)
    CreationDate = Column(Text, nullable=False, server_default=func.now())


class Categories(Base):
    __tablename__ = 'Categories'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(Text, nullable=False)
    Image = Column(Text, nullable=True)
    ParentId = Column(ForeignKey("Categories.Id", ondelete="CASCADE"), nullable=True, default=None)
    Type = Column(Enum(ContentTypes), nullable=False)
    Active = Column(Boolean(), nullable=False, default=True)
    OrderBy = Column(Integer, nullable=True)
    CreationDate = Column(Text, nullable=False, server_default=func.now())


class Agents(Base):
    __tablename__ = 'Agents'
    Id = Column(BigInteger, primary_key=True, autoincrement=True)
    EpisodeId = Column(ForeignKey("DocumentsEpisodes.Id", ondelete="CASCADE"), nullable=False)
    ArtistId = Column(ForeignKey("Artists.Id", ondelete="CASCADE"), nullable=True)
    Name = Column(Text, nullable=True)
    IsMain = Column(Boolean(), nullable=False, default=False)
    OrderBy = Column(Integer, nullable=True)
    CreationDate = Column(Text, nullable=False, server_default=func.now())


class AgentRoles(Base):
    __tablename__ = 'AgentRoles'
    Id = Column(BigInteger, primary_key=True, autoincrement=True)
    AgentId = Column(ForeignKey("Agents.Id", ondelete="CASCADE"), nullable=False)
    Role = Column(Enum(AgentRolesEntities), nullable=False)
    OrderBy = Column(Integer, nullable=True)
    CreationDate = Column(Text, nullable=False, server_default=func.now())


class UsersTemp(Base):
    __tablename__ = 'UsersTemp'
    Id = Column(BigInteger, primary_key=True, autoincrement=True)
    Phone = Column(Text, nullable=False)
    VerifyCode = Column(Text, nullable=False)
    CreationDate = Column(Text, nullable=False, server_default=func.now())


class Artists(Base):
    __tablename__ = 'Artists'
    Id = Column(BigInteger, primary_key=True, autoincrement=True)
    DirectoryName = Column(Text, unique=True, nullable=False, default=lambda: uuid.uuid4().hex)
    ProfileImage = Column(Text, nullable=True)
    Name = Column(Text, nullable=False)
    Active = Column(Boolean(), nullable=False, default=True)
    ContentType = Column(Enum(ContentTypes), nullable=False)
    CreationDate = Column(Text, nullable=False, server_default=func.now())


class ArtistImages(Base):
    __tablename__ = 'ArtistImages'
    Id = Column(BigInteger, primary_key=True, autoincrement=True)
    ArtistId = Column(ForeignKey("Artists.Id", ondelete="CASCADE"), nullable=False)
    Image = Column(Text, nullable=False)
    OrderBy = Column(Integer, nullable=True)
    CreationDate = Column(Text, nullable=False, server_default=func.now())


class ArtistLinks(Base):
    __tablename__ = 'ArtistLinks'
    Id = Column(BigInteger, primary_key=True, autoincrement=True)
    ArtistId = Column(ForeignKey("Artists.Id", ondelete="CASCADE"), nullable=False)
    Title = Column(Text, nullable=True)
    Url = Column(Text, nullable=True)
    Type = Column(Enum(Socials), nullable=True)
    OrderBy = Column(Integer, nullable=True)
    CreationDate = Column(Text, nullable=False, server_default=func.now())


class Users(Base):
    __tablename__ = 'Users'
    Id = Column(BigInteger, primary_key=True, autoincrement=True)
    DirectoryName = Column(Text, unique=True, nullable=False, default=lambda: uuid.uuid4().hex)
    ProfileImage = Column(Text, nullable=True)
    Name = Column(Text, nullable=False)
    Phone = Column(Text, unique=True, nullable=True)
    UserName = Column(Text, unique=True, nullable=False, default=lambda: uuid.uuid4().hex[:16])
    Password = Column(Text, nullable=False)
    Email = Column(Text, unique=True, nullable=True)
    Active = Column(Boolean(), nullable=False, default=True)
    CreationDate = Column(Text, nullable=False, server_default=func.now())


class UserLikes(Base):
    __tablename__ = 'UserLikes'
    Id = Column(BigInteger, primary_key=True, autoincrement=True)
    UserId = Column(ForeignKey("Users.Id", ondelete="CASCADE"), nullable=False)
    DocumentId = Column(ForeignKey("Document.Id", ondelete="CASCADE"), nullable=False)
    EpisodeId = Column(ForeignKey("DocumentsEpisodes.Id", ondelete="CASCADE"), nullable=False)
    CreationDate = Column(Text, nullable=False, server_default=func.now())


class PlayList(Base):
    __tablename__ = 'PlayList'
    Id = Column(BigInteger, primary_key=True, autoincrement=True)
    Title = Column(Text, nullable=False)
    Description = Column(Text, nullable=True)
    OwnerUser = Column(ForeignKey("Users.Id", ondelete="CASCADE"), nullable=False)
    Public = Column(Boolean(), nullable=False, default=False)
    CreationDate = Column(Text, nullable=False, server_default=func.now())


class PlayListRepository(Base):
    __tablename__ = 'PlayListRepository'
    Id = Column(BigInteger, primary_key=True, autoincrement=True)
    PlayListId = Column(ForeignKey("PlayList.Id", ondelete="CASCADE"), nullable=False)
    DocumentId = Column(ForeignKey("Document.Id", ondelete="CASCADE"), nullable=False)
    EpisodesId = Column(ForeignKey("DocumentsEpisodes.Id", ondelete="CASCADE"), nullable=False)
    OrderBy = Column(Integer, nullable=True)
    CreationDate = Column(Text, nullable=False, server_default=func.now())


class UserFollowing(Base):
    __tablename__ = 'UserFollowing'
    Id = Column(BigInteger, primary_key=True)
    UserId = Column(ForeignKey("Users.Id", ondelete="CASCADE"), nullable=False)
    ArtistId = Column(ForeignKey("Artists.Id", ondelete="CASCADE"), nullable=True)
    DocumentId = Column(ForeignKey("Document.Id", ondelete="CASCADE"), nullable=True)
    PlayListId = Column(ForeignKey("PlayList.Id", ondelete="CASCADE"), nullable=True)
    CreationDate = Column(Text, nullable=False, server_default=func.now())


class MetaData(Base):
    __tablename__ = 'MetaData'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    MarketAppLink = Column(Text, nullable=True)
    AboutUs = Column(Text, nullable=True)
    ContactUs = Column(Text, nullable=True)
    PrivacyAndTerms = Column(Text, nullable=True)
    CreationDate = Column(Text, nullable=False, server_default=func.now())


class SocialLinks(Base):
    __tablename__ = 'SocialLinks'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Title = Column(Text, nullable=True)
    Url = Column(Text, nullable=True)
    Type = Column(Enum(Socials), nullable=True)
    OrderBy = Column(Integer, nullable=True)
    CreationDate = Column(Text, nullable=False, server_default=func.now())
