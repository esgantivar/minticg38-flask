from bson import DBRef, ObjectId

from models.abstract import AbstractModel, ItemDoesNotExist
from models.deparment import Department
from utils import parse_object_id


class Subject(AbstractModel):
    COLLECTION_NAME = "subjects"

    name = None
    course_credits = None
    department: Department = None

    def __init__(self, name, course_credits, department=None, _id=None):
        super().__init__(_id)
        self.name = name
        self.course_credits = course_credits
        self.department = department

    def prepare_to_save(self):
        return {
            "name": self.name,
            "course_credits": self.course_credits,
            "department": DBRef(
                id=ObjectId(self.department._id),
                collection=Department.COLLECTION_NAME
            ) if self.department else None
        }

    @staticmethod
    def factory(doc):
        department = None
        if doc.get("department"):
            department = Department.factory(doc.get("department"))
        return Subject(
            name=doc["name"],
            course_credits=doc["course_credits"],
            department=department,
            _id=parse_object_id(doc["_id"])
        )

    def to_json(self):
        data = self.__dict__
        if self.department:
            data["department"] = self.department.__dict__
        return data


class SubjectDoesNotExist(ItemDoesNotExist):
    pass
