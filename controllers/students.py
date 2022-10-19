from bson import ObjectId

from controllers.abstract import CRUDController
from models.student import Student
from pymongo import MongoClient

MONGO_STRING_CONNECTION = "mongodb+srv://minticg38:ciclo4a2022@clusterg38.veo0jfn.mongodb.net/?retryWrites=true&w=majority"


class StudentsController(CRUDController):

    def __init__(self):
        self._client = MongoClient(MONGO_STRING_CONNECTION)
        self.database = self._client.get_database("academic")
        self.collection = self.database.get_collection(Student.COLLECTION_NAME)
        self._items = []

    def get_all(self):
        _students = []
        for doc in self.collection.find():
            doc["_id"] = str(doc["_id"])
            _students.append(
                Student(
                    cedula=doc["cedula"],
                    last_name=doc["last_name"],
                    first_name=doc["first_name"],
                    email=doc["email"],
                    _id=doc["_id"],
                )
            )
        return _students

    def get_by_id(self, id_student):
        doc = self.collection.find_one({
            "_id": ObjectId(id_student)
        })
        if doc is None:
            raise StudentDoesNotExist
        return Student(
            cedula=doc["cedula"],
            last_name=doc["last_name"],
            first_name=doc["first_name"],
            email=doc["email"],
            _id=str(doc["_id"]),
        )

    def create(self, content):
        created = Student(
            cedula=content["cedula"],
            first_name=content["first_name"],
            last_name=content["last_name"],
            email=content["email"]
        )
        inserted = self.collection.insert_one({
            "cedula": created.cedula,
            "first_name": created.first_name,
            "last_name": created.last_name,
            "email": created.email
        })
        created._id = str(inserted.inserted_id)
        return created

    def update(self, id_student, content):
        student = self.get_by_id(id_student)
        student.cedula = content["cedula"]
        student.first_name = content["first_name"]
        student.last_name = content["last_name"]
        student.email = content["email"]
        self.collection.update_one({
            "_id": ObjectId(student._id)
        }, {
            "$set": {
                "cedula": student.cedula,
                "first_name": student.first_name,
                "last_name": student.last_name,
                "email": student.email
            }
        })
        return student

    def delete(self, id_student):
        delete_result = self.collection.delete_one({
            "_id": ObjectId(id_student)
        })
        return delete_result.deleted_count

    def count(self):
        return self.collection.count_documents({})

    def _find_index(self, value_key):
        for idx, value in enumerate(self._items):
            if value._id == value_key:
                return idx
        raise StudentDoesNotExist


class StudentDoesNotExist(Exception):
    pass
