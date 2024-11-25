from sqlalchemy.sql import text
import config
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from constants import *
import os


def create_directories():

    path = Directories.temp
    if not os.path.exists(path):
        os.mkdir(path)


# ================ CREATE DATABASE IF NOT EXISTS ================
# def create_db():
#     URL = f"mariadb+mariadbconnector://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/"
#     # URL = "postgresql://root:ZHqPsIiG4ZX9e29CkmEgoAY7@chogolisa.liara.cloud:30333/"
#     sql = text("CREATE DATABASE %s" % config.DB_NAME)
#     engine_ = create_engine(URL)
#     with engine_.connect() as con:
#         con.execute(sql)
#         con.close()
#     pass


# ================================================================
# DATABASE_URL = f"mariadb+mariadbconnector://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
DATABASE_URL = f"postgresql://root:ZHqPsIiG4ZX9e29CkmEgoAY7@chogolisa.liara.cloud:30333/{config.DB_NAME}"

engine = create_engine(DATABASE_URL)

Base = declarative_base()

sessionLocal = sessionmaker(bind=engine)
