from abc import ABC
from typing import Type

from bson import ObjectId, DBRef
from pymongo import MongoClient

from models.abstract import AbstractModel

MONGO_STRING_CONNECTION = "mongodb+srv://minticg38:ciclo4a2022@clusterg38.veo0jfn.mongodb.net/?retryWrites=true&w=majority"
DATABASE_NAME = "academico"


class AbstractRepository(ABC):
    def __init__(self, model: Type[AbstractModel]):
        self._client = MongoClient(MONGO_STRING_CONNECTION)
        self.database = self._client.get_database(DATABASE_NAME)
        self.collection = self.database.get_collection(model.COLLECTION_NAME)
        self.model = model

    def save(self, item: AbstractModel):
        if item.is_new():
            inserted = self.collection.insert_one(
                item.prepare_to_save()
            )
            item._id = str(inserted.inserted_id)
        else:
            self.collection.update_one({
                "_id": ObjectId(item._id)
            }, {
                "$set": item.prepare_to_save()
            })
        return item

    def delete(self, item: AbstractModel):
        response = self.collection.delete_one({
            "_id": ObjectId(item._id)
        })
        return {
            "deleted_count": response.deleted_count
        }

    def get_all(self):
        items = []
        for doc in self.collection.find():
            self._fill_db_ref(doc)
            items.append(self.model.create(doc))
        return items

    def get_by_id(self, id_item):
        doc = self.collection.find_one({
            "_id": ObjectId(id_item)
        })
        if not doc:
            raise Exception
        self._fill_db_ref(doc)
        return self.model.create(doc)

    def count(self):
        return self.collection.count_documents({})

    def _fill_db_ref(self, doc):
        for key, value in doc.items():
            if value and isinstance(value, DBRef):
                collection = self.database.get_collection(value.collection)
                doc_related = collection.find_one({
                    "_id": value.id
                })
                doc[key] = doc_related
