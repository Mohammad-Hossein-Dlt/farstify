import datetime
import uuid

from sqlalchemy import ForeignKey, Column, Text, Boolean, Enum, Integer, BigInteger, DateTime, func, DATETIME
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import ulid
from database import *
from constants import *


class Task(Base):
    __tablename__ = 'Task'
    Id = Column(BigInteger, primary_key=True, autoincrement=True)
    ArtistId = Column(ForeignKey("Artists.Id", ondelete="CASCADE"), nullable=False)
    EpisodeId = Column(ForeignKey("DocumentsEpisodes.Id", ondelete="CASCADE"), nullable=False)
    # File = Column(ForeignKey("DocumentsEpisodes.File", ondelete="CASCADE"), nullable=False)
    ActionState = Column(Enum(ProcessActionTaskState), nullable=False)
    CreationDate = Column(DateTime, nullable=False, server_default=func.now())


class Document(Base):
    __tablename__ = 'Document'
    Id = Column(BigInteger, primary_key=True, autoincrement=True)
    Owner = Column(ForeignKey("Artists.Id", ondelete="CASCADE"), nullable=False)
    DirectoryName = Column(Text, unique=True, nullable=False, default=ulid.new().str)
    Name = Column(Text, nullable=False)
    MainImage = Column(Text, nullable=True)
    Description = Column(Text, nullable=True)
    ContentType = Column(Enum(ContentTypes), nullable=False)
    Active = Column(Boolean(), nullable=False, default=True)
    Single = Column(Boolean(), nullable=False, default=True)
    CreationDate = Column(Text, nullable=False, server_default=func.now())

    # episodes = relationship("DocumentsEpisodes", backref="Document")
    contributors = relationship("Contributors", backref="Document")


class DocumentsLinks(Base):
    __tablename__ = 'DocumentsLinks'
    Id = Column(BigInteger, primary_key=True, autoincrement=True)
    DocumentId = Column(ForeignKey("Document.Id", ondelete="CASCADE"), nullable=False)
    Title = Column(Text, nullable=True)
    Link = Column(Text, nullable=True)
    OrderBy = Column(Integer, nullable=True)


class DocumentsEpisodes(Base):
    __tablename__ = 'DocumentsEpisodes'
    Id = Column(BigInteger, primary_key=True, autoincrement=True)
    Title = Column(Text, nullable=False)
    Image = Column(Text, nullable=True)
    File = Column(Text, nullable=True)
    Duration = Column(BigInteger, nullable=False, default=0)
    DocumentId = Column(ForeignKey("Document.Id", ondelete="CASCADE"), nullable=False)
    OrderBy = Column(Integer, nullable=True)
    CreationDate = Column(Text, nullable=False, server_default=func.now())


class ListenedHistory(Base):
    __tablename__ = 'ListenedHistory'
    Id = Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4())
    UserId = Column(ForeignKey("Users.Id", ondelete="CASCADE"), nullable=False)
    ArtistsId = Column(ForeignKey("Artists.Id", ondelete="CASCADE"), nullable=False)
    EpisodeId = Column(ForeignKey("DocumentsEpisodes.Id", ondelete="CASCADE"), nullable=False)
    DocumentId = Column(ForeignKey("Document.Id", ondelete="CASCADE"), nullable=False)
    CreationDate = Column(Text, nullable=False, server_default=func.now())


class DocumentsLabels(Base):
    __tablename__ = 'DocumentsLabels'
    Id = Column(BigInteger, primary_key=True, autoincrement=True)
    Title = Column(Text, nullable=False)
    DocumentId = Column(ForeignKey("Document.Id", ondelete="CASCADE"), nullable=False)


class Contributors(Base):
    __tablename__ = 'Contributors'
    Id = Column(BigInteger, primary_key=True, autoincrement=True)
    OwnerId = Column(ForeignKey("Artists.Id", ondelete="CASCADE"), nullable=False)
    ArtistId = Column(ForeignKey("Artists.Id", ondelete="CASCADE"), nullable=False)
    DocumentId = Column(ForeignKey("Document.Id", ondelete="CASCADE"), nullable=True)
    CreationDate = Column(Text, nullable=False, server_default=func.now())


class Categories(Base):
    __tablename__ = 'Categories'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(Text, nullable=False)
    Image = Column(Text, nullable=True)
    Active = Column(Boolean(), nullable=False, default=True)
    ParentId = Column(ForeignKey("Categories.Id", ondelete="CASCADE"), nullable=True, default=None)
    Type = Column(Enum(ContentTypes), nullable=False)
    OrderBy = Column(Integer, nullable=True)


class DocumentsCategories(Base):
    __tablename__ = 'DocumentsCategories'
    Id = Column(BigInteger, primary_key=True, autoincrement=True)
    CategoryId = Column(ForeignKey("Categories.Id", ondelete="CASCADE"), nullable=False)
    DocumentId = Column(ForeignKey("Document.Id", ondelete="CASCADE"), nullable=False)
    OrderBy = Column(Integer, nullable=True)


# class Subscriptions(Base):
#     __tablename__ = 'Subscriptions'
#     Id = Column(Integer, primary_key=True, autoincrement=True)
#     Title = Column(Text, nullable=False)
#     Price = Column(Text, nullable=False)
#     Period = Column(Integer, nullable=False)
#     Discount = Column(Integer, nullable=False, default=0)
#     IsPremiumSubscription = Column(Enum(BoolEnum), nullable=False, default=BoolEnum.false)
#     DiscountCodeApply = Column(Enum(BoolEnum), nullable=False, default=BoolEnum.true)#

# class DiscountCodes(Base):
#     __tablename__ = 'DiscountCodes'
#     Id = Column(Integer, primary_key=True, autoincrement=True)
#     Code = Column(Text, nullable=False)
#     OrdinaryPercent = Column(Integer, nullable=False, default=0)
#     PremiumPercent = Column(Integer, nullable=False, default=0)

class Agents(Base):
    __tablename__ = 'Agents'
    Id = Column(BigInteger, primary_key=True, autoincrement=True)
    OwnerId = Column(ForeignKey("Artists.Id", ondelete="CASCADE"), nullable=False)
    EpisodeId = Column(ForeignKey("DocumentsEpisodes.Id", ondelete="CASCADE"), nullable=False)
    ArtistId = Column(ForeignKey("Artists.Id", ondelete="CASCADE"), nullable=True)
    Name = Column(Text, nullable=True)
    IsMain = Column(Boolean(), nullable=False, default=False)
    OrderBy = Column(Integer, nullable=True)

    roles = relationship("AgentRoles", backref="agent_roles")


class AgentRoles(Base):
    __tablename__ = 'AgentRoles'
    Id = Column(BigInteger, primary_key=True, autoincrement=True)
    AgentId = Column(ForeignKey("Agents.Id", ondelete="CASCADE"), nullable=True)
    Role = Column(Enum(AgentRolesEntities), nullable=False)
    OrderBy = Column(Integer, nullable=True)


class UsersTemp(Base):
    __tablename__ = 'UsersTemp'
    Id = Column(BigInteger, primary_key=True, autoincrement=True)
    Phone = Column(Text, nullable=False)
    VerifyCode = Column(Text, nullable=False)
    Date = Column(DateTime, nullable=False, server_default=func.now())


class Artists(Base):
    __tablename__ = 'Artists'
    # Id = Column(UUID(as_uuid=True), unique=True, primary_key=True, default=str(ulid.new().uuid))
    Id = Column(BigInteger, primary_key=True, autoincrement=True)
    DirectoryName = Column(Text, unique=True, nullable=False, default=ulid.new().str)
    ProfileImage = Column(Text, nullable=True)
    Name = Column(Text, nullable=False)
    Active = Column(Boolean(), nullable=False, default=True)
    ContentType = Column(Enum(ContentTypes), nullable=False)
    Date = Column(Text, nullable=False, default=datetime.datetime.now())


class ArtistImages(Base):
    __tablename__ = 'ArtistImages'
    Id = Column(BigInteger, primary_key=True, autoincrement=True)
    ArtistId = Column(ForeignKey("Artists.Id", ondelete="CASCADE"), nullable=False)
    Image = Column(Text, nullable=False)
    OrderBy = Column(Integer, nullable=True)


class ArtistLinks(Base):
    __tablename__ = 'ArtistLinks'
    Id = Column(BigInteger, primary_key=True, autoincrement=True)
    Title = Column(Text, nullable=True)
    ArtistId = Column(ForeignKey("Artists.Id", ondelete="CASCADE"), nullable=False)
    Link = Column(Text, nullable=True)
    OrderBy = Column(Integer, nullable=True)


class Users(Base):
    __tablename__ = 'Users'
    Id = Column(BigInteger, primary_key=True, autoincrement=True)
    DirectoryName = Column(Text, unique=True, nullable=False, default=ulid.new().str)
    ProfileImage = Column(Text, nullable=True)
    Name = Column(Text, nullable=False)
    Phone = Column(Text, unique=True, nullable=True)
    UserName = Column(Text, unique=True, nullable=False, default=ulid.new().str)
    Password = Column(Text, nullable=False)
    Email = Column(Text, unique=True, nullable=True)
    Active = Column(Boolean(), nullable=False, default=True)
    RegistryDate = Column(Text, nullable=False, default=datetime.datetime.now())


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
    Title = Column(Text, nullable=True)
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


class UserFollowing(Base):
    __tablename__ = 'UserFollowing'
    Id = Column(BigInteger, primary_key=True)
    UserId = Column(ForeignKey("Users.Id", ondelete="CASCADE"), nullable=False)
    ArtistId = Column(ForeignKey("Artists.Id", ondelete="CASCADE"), nullable=True)
    DocumentId = Column(ForeignKey("Document.Id", ondelete="CASCADE"), nullable=True)
    PlayListId = Column(ForeignKey("PlayList.Id", ondelete="CASCADE"), nullable=True)
    CreationDate = Column(Text, nullable=False, server_default=func.now())


class HomePageItems(Base):
    __tablename__ = 'HomePageItems'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Title = Column(Text, nullable=True)
    Type = Column(Enum(ContentTypes), nullable=False)
    SortedBy = Column(Enum(SortBy), nullable=False, default=SortBy.artist)
    OrderBy = Column(Enum(OrderBy), nullable=False, default=OrderBy.asc)
    CategoryId = Column(ForeignKey("Categories.Id", ondelete="CASCADE"), nullable=True)


class HomePageDocumentsRepository(Base):
    __tablename__ = 'HomePageDocumentsRepository'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    DocumentId = Column(ForeignKey("Document.Id", ondelete="CASCADE"), nullable=False)
    HomePageItemId = Column(ForeignKey("HomePageItems.Id", ondelete="CASCADE"), nullable=False)


class MetaData(Base):
    __tablename__ = 'MetaData'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    MarketAppLink = Column(Text, nullable=True)
    AboutUs = Column(Text, nullable=True)
    ContactUs = Column(Text, nullable=True)
    PrivacyAndTerms = Column(Text, nullable=True)


class SocialLink(Base):
    __tablename__ = 'SocialLink'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Title = Column(Text, nullable=True)
    Type = Column(Enum(Socials), nullable=True)
    Link = Column(Text, nullable=True)
