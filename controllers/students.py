from controllers.abstract import CRUDController
from models.student import Student
from pymongo import MongoClient

MONGO_STRING_CONNECTION = "mongodb+srv://minticg38:ciclo4a2022@clusterg38.veo0jfn.mongodb.net/?retryWrites=true&w=majority"


class StudentsController(CRUDController):

    def __init__(self):
        self._client = MongoClient(MONGO_STRING_CONNECTION)
        self.database = self._client.get_database("academic")
        self.collection = self.database.get_collection("students")
        self._items = []

    def get_all(self):
        return self._items

    def get_by_id(self, id_student):
        index = self._find_index(id_student)
        return self._items[index]

    def create(self, content):
        inserted = self.collection.insert_one({
            "cedula": content["cedula"],
            "first_name": content["first_name"],
            "last_name": content["last_name"],
            "email": content["email"]
        })
        created = Student(
            _id=str(inserted.inserted_id),
            cedula=content["cedula"],
            first_name=content["first_name"],
            last_name=content["last_name"],
            email=content["email"]
        )
        self._items.append(created)
        return created

    def update(self, id_student, content):
        index = self._find_index(id_student)
        selected = self._items[index]
        selected.cedula = content["cedula"]
        selected.first_name = content["first_name"]
        selected.last_name = content["last_name"]
        selected.email = content["email"]
        return selected

    def delete(self, id_student):
        index = self._find_index(id_student)
        self._items.pop(index)

    def count(self):
        return len(self._items)

    def _find_index(self, value_key):
        for idx, value in enumerate(self._items):
            if value._id == value_key:
                return idx
        raise StudentDoesNotExist


class StudentDoesNotExist(Exception):
    pass
