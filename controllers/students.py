from controllers.abstract import CRUDController
from models.student import Student, StudentDoesNotExist

from repositories.student import StudentRepository


class StudentsController(CRUDController):

    def __init__(self):
        self.repository = StudentRepository(
            model=Student,
            does_not_exist=StudentDoesNotExist
        )

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id_student):
        return self.repository.get_by_id(id_student)

    def create(self, content):
        created = Student(
            cedula=content["cedula"],
            first_name=content["first_name"],
            last_name=content["last_name"],
            email=content["email"]
        )
        return self.repository.save(created)

    def update(self, id_student, content):
        student = self.get_by_id(id_student)
        student.cedula = content["cedula"]
        student.first_name = content["first_name"]
        student.last_name = content["last_name"]
        student.email = content["email"]
        return self.repository.save(student)

    def delete(self, id_student):
        student = self.get_by_id(id_student)
        return self.repository.delete(student)

    def count(self):
        return self.repository.count()

    def assign_auth_id(self, id_student, auth_id):
        student = self.get_by_id(id_student)
        student.auth_id = auth_id
        return self.repository.save(student)
