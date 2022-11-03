from bson import ObjectId

from controllers.abstract import CRUDController
from models.registration import Registration, RegistrationDoesNotExist
from models.student import Student, StudentDoesNotExist
from models.subject import Subject, SubjectDoesNotExist
from repositories.registration import RegistrationRepository
from repositories.student import StudentRepository
from repositories.subject import SubjectRepository


class RegistrationsController(CRUDController):

    def __init__(self):
        self.repository = RegistrationRepository(
            Registration,
            RegistrationDoesNotExist
        )
        self.r_subject = SubjectRepository(
            Subject,
            SubjectDoesNotExist
        )
        self.r_student = StudentRepository(
            Student,
            StudentDoesNotExist
        )

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id_element):
        return self.repository.get_by_id(id_element)

    def create(self, content):
        """
        {
            "grade": 5,
            "semester": "II",
            "year": 2022,
            "subject": {
                "id": "...",
            },
            "student": {
                "id": "...",
            }
        }
        """
        doc_student = content.get("student", {})
        doc_subject = content.get("subject", {})
        content["student"] = self.r_student.get_by_id(doc_student.get("id")).to_json()
        content["subject"] = self.r_subject.get_by_id(doc_subject.get("id")).to_json()
        return self.repository.save(
            item=Registration.create(content)
        )

    def update(self, id_element, content):
        element = self.get_by_id(id_element)
        element.year = content["year"]
        element.semester = content["semester"]
        element.grade = content["grade"]
        doc_student = content.get("student", {})
        doc_subject = content.get("subject", {})
        element.student = self.r_student.get_by_id(doc_student.get("id"))
        element.subject = self.r_subject.get_by_id(doc_subject.get("id"))
        return self.repository.save(element)

    def delete(self, id_element):
        element = self.get_by_id(id_element)
        return self.repository.delete(element)

    def count(self):
        return self.repository.count()

    def calc_avg_subject(self, id_subject, year, semester):
        pipeline = [
            {
                '$match': {
                    'subject.$id': ObjectId(id_subject),
                    'year': year,
                    'semester': semester
                }
            }, {
                '$group': {
                    '_id': '$subject',
                    'average': {
                        '$avg': '$grade'
                    }
                }
            }
        ]

        return self.repository.calc_aggregation(pipeline)

    def delete_by_student(self, id_student):
        return self.repository.delete_many({
            "student.$id": ObjectId(id_student)
        })
