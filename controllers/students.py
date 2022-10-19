from controllers.abstract import CRUDController
from models.student import Student

from repositories.student import StudentRepository


class StudentsController(CRUDController):

    def __init__(self):
        self.repo = StudentRepository(model=Student)

    def get_all(self):
        return self.repo.get_all()

    def get_by_id(self, id_student):
        return self.repo.get_by_id(id_student)

    def create(self, content):
        return self.repo.save(
            item=Student(
                cedula=content["cedula"],
                first_name=content["first_name"],
                last_name=content["last_name"],
                email=content["email"]
            )
        )

    def update(self, id_student, content):
        student = self.get_by_id(id_student)
        student.cedula = content["cedula"]
        student.first_name = content["first_name"]
        student.last_name = content["last_name"]
        student.email = content["email"]
        return self.repo.save(student)

    def delete(self, id_student):
        return self.delete(id_student)

    def count(self):
        return self.repo.count()