from bson import ObjectId, DBRef
from pymongo import MongoClient

from models.registration import Registration, RegistrationDoesNotExist
from repositories.abstract import AbstractRepository

MONGO_STRING_CONNECTION = "mongodb+srv://minticg38:ciclo4a2022@clusterg38.veo0jfn.mongodb.net/?retryWrites=true&w=majority"
DATABASE_NAME = "academico"





class RegistrationRepository(AbstractRepository):
    pass