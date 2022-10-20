from controllers.abstract import CRUDController
from models.deparment import Department, DepartmentDoesNotExist
from repositories.deparment import DepartmentRepository


class DepartmentsController(CRUDController):

    def __init__(self):
        self.repo = DepartmentRepository(
            model=Department,
            exception=DepartmentDoesNotExist
        )

    def get_all(self):
        return self.repo.get_all()

    def get_by_id(self, id_department):
        return self.repo.get_by_id(id_department)

    def create(self, content):
        return self.repo.save(
            item=Department.factory(content)
        )

    def update(self, id_department, content):
        element = self.get_by_id(id_department)
        element.name = content["name"]
        element.description = content["description"]
        return self.repo.save(element)

    def delete(self, id_department):
        student = self.get_by_id(id_department)
        return self.repo.delete(student)

    def count(self):
        return self.repo.count()
