import os
from abc import ABC
from typing import Type

from bson import ObjectId, DBRef
from dotenv import load_dotenv
from pymongo import MongoClient

from models.abstract import AbstractModel, ItemDoesNotExist

load_dotenv()

MONGO_STRING_CONNECTION = os.environ.get("MONGO_STRING_CONNECTION")
DATABASE_NAME = os.environ.get("DATABASE_NAME")


class AbstractRepository(ABC):
    def __init__(
            self,
            model: Type[AbstractModel],
            exception: Type[ItemDoesNotExist]=ItemDoesNotExist
    ):
        self._client = MongoClient(MONGO_STRING_CONNECTION)
        self.database = self._client.get_database(DATABASE_NAME)
        self.collection = self.database.get_collection(model.COLLECTION_NAME)
        self.model = model
        self.exception = exception

    def save(self, item: AbstractModel):
        if item.is_new:
            inserted = self.collection.insert_one(item.prepare_to_save())
            item._id = str(inserted.inserted_id)
        else:
            self.collection.update_one({
                "_id": item.object_id
            }, {
                "$set": item.prepare_to_save()
            })
        return item

    def update(self, item: AbstractModel):
        response = self.collection.update_one({
            "_id": item.object_id
        }, {
            "$set": item.prepare_to_save()
        })
        return {"updated_count": response.modified_count}

    def delete(self, item: AbstractModel):
        response = self.collection.delete_one({
            "_id": item.object_id
        })
        return {
            "deleted_count": response.deleted_count
        }

    def get_all(self):
        items = []
        for doc in self.collection.find():
            self._handle_db_ref(doc)
            items.append(self.model.factory(doc))
        return items

    def get_by_id(self, id_item):
        doc = self.collection.find_one({
            "_id": ObjectId(id_item)
        })
        if doc is None:
            raise self.exception
        self._handle_db_ref(doc)
        return self.model.factory(doc)

    def _handle_db_ref(self, doc):
        for key, value in doc.items():
            if isinstance(value, DBRef):
                collection = self.database.get_collection(value.collection)
                doc_related = collection.find_one({
                    "_id": value.id
                })
                if doc_related:
                    doc[key] = doc_related

    def count(self):
        return self.collection.count_documents({})
