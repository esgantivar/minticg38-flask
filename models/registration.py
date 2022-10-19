from bson import DBRef, ObjectId

from models.abstract import AbstractModel, ItemDoesNotExist
from models.student import Student
from models.subject import Subject


class Registration(AbstractModel):
    COLLECTION_NAME = "registrations"
    year = None
    semester = None
    grade = None
    student: Student = None
    subject: Subject = None

    def __init__(self,
                 year,
                 semester,
                 student,
                 subject,
                 grade=0,
                 _id=None):
        super().__init__(_id)
        self.year = year
        self.semester = semester
        self.grade = grade
        self.student = student
        self.subject = subject

    @staticmethod
    def factory(doc):
        return Registration

    def prepare_to_save(self):
        return {
            "year": self.year,
            "semester": self.semester,
            "grade": self.grade,
            "student": DBRef(
                id=ObjectId(self.student._id),
                collection=Student.COLLECTION_NAME
            ),
            "subject": DBRef(
                id=ObjectId(self.subject._id),
                collection=Subject.COLLECTION_NAME
            )
        }

    def to_json(self):
        pass


class RegistrationDoesNotExist(ItemDoesNotExist):
    pass
