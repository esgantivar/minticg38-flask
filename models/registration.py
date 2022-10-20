from bson import DBRef, ObjectId

from models.abstract import AbstractModel
from models.student import Student
from models.subject import Subject


class Registration(AbstractModel):
    COLLECTION_NAME = "registrations"

    year: int = None
    semester: int = None
    grade: float = None
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
        return {
            "year": self.year,
            "semester": self.semester,
            "grade": self.grade,
            "student": self.student.to_json(),
            "subject": self.subject.to_json()
        }

    @staticmethod
    def create(doc):
        assert doc.get("subject")
        assert doc.get("student")
        subject = Subject.create(doc.get("subject"))
        student = Student.create(doc.get("student"))
        return Registration(
            year=doc.get("year"),
            semester=doc.get("semester"),
            grade=doc.get("grade", 0),
            subject=subject,
            student=student
        )


class RegistrationDoesNotExist(Exception):
    pass


