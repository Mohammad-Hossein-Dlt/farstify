from constants import Directories
from pydantic import BaseModel
from typing import Annotated
from fastapi import Depends
from utills.path_manager import make_path
import uuid
import os
import shutil


def init_temp_directory(directory_name: str):
    path = make_path(Directories.temp, directory_name, is_file=False)
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def delete_temp(directory_name: str):
    path = make_path(Directories.temp, directory_name, is_file=False)
    if path.replace("/", "") != Directories.temp.replace("/", "") and os.path.exists(path):
        shutil.rmtree(path)
        return path


class Temp(BaseModel):
    name: str
    path: str
    auto_delete: bool = True

    def delete(self):
        delete_temp(self.name)


def auto_delete_temp():
    name = uuid.uuid4().hex
    path = init_temp_directory(name)
    temp = Temp(name=name, path=path)
    try:
        yield temp
    finally:
        delete_temp(name)


auto_delete_temp_dependency = Annotated[Temp, Depends(auto_delete_temp)]


def manual_delete_temp():
    name = uuid.uuid4().hex
    try:
        path = init_temp_directory(name)
        temp = Temp(name=name, path=path)
        yield temp
    finally:
        pass


manual_delete_temp_dependency = Annotated[Temp, Depends(manual_delete_temp)]
