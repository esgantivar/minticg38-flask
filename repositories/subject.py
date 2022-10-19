import os

from repositories.abstract import AbstractRepository

MONGO_STRING_CONNECTION = os.environ.get("MONGO_STRING_CONNECTION")
DATABASE_NAME = os.environ.get("DATABASE_NAME")


class SubjectRepository(AbstractRepository):
    pass
