from controllers.abstract import CRUDController
from models.deparment import Department, DepartmentDoesNotExist
from repositories.department import DepartmentRepository


class DepartmentsController(CRUDController):

    def __init__(self):
        self.repository = DepartmentRepository(
            model=Department,
            does_not_exist=DepartmentDoesNotExist
        )

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id_item):
        return self.repository.get_by_id(id_item)

    def create(self, content):
        return self.repository.save(
            Department.create(content)
        )

    def update(self, id_item, content):
        department = self.get_by_id(id_item)
        department.name = content["name"]
        department.description = content["description"]
        return self.repository.save(department)

    def delete(self, id_item):
        department = self.get_by_id(id_item)
        return self.repository.delete(department)

    def count(self):
        return self.repository.count()
