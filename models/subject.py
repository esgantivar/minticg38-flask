from bson import DBRef, ObjectId

from models.abstract import AbstractModel, ElementDoesNotExist
from models.deparment import Department


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
        department_db_ref = None
        if self.department:
            department_db_ref = DBRef(
                id=ObjectId(self.department._id),
                collection=Department.COLLECTION_NAME
            )
        return {
            "name": self.name,
            "course_credits": self.course_credits,
            "department": department_db_ref
        }

    def to_json(self):
        department = None
        if self.department:
            department = self.department.to_json()
        return {
            "_id": self._id,
            "name": self.name,
            "course_credits": self.course_credits,
            "department": department
        }

    @staticmethod
    def create(doc):
        department = None
        if doc.get("department"):
            department = Department.create(doc.get("department"))
        return Subject(
            name=doc["name"],
            course_credits=doc["course_credits"],
            department=department,
            _id=str(doc["_id"]) if doc.get("_id") else None,
        )


class SubjectDoesNotExist(ElementDoesNotExist):
    pass
