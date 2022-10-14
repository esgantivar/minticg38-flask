from controllers.abstract import CRUDController
from models.student import Student


class StudentsController(CRUDController):

    def __init__(self):
        self._items = []

    def get_all(self):
        return self._items

    def get_by_id(self, id_student):
        index = self._find_index(id_student)
        return self._items[index]

    def create(self, content):
        created = Student(
            _id=content["_id"],
            cedula=content["cedula"],
            first_name=content["first_name"],
            last_name=content["last_name"],
            email=content["email"]
        )
        self._items.append(created)
        return created

    def update(self, id_student, content):
        index = self._find_index(id_student)
        selected = self._items[index]
        selected.cedula = content["cedula"]
        selected.first_name = content["first_name"]
        selected.last_name = content["last_name"]
        selected.email = content["email"]
        return selected

    def delete(self, id_student):
        index = self._find_index(id_student)
        self._items.pop(index)

    def count(self):
        return len(self._items)

    def _find_index(self, value_key):
        for idx, value in enumerate(self._items):
            if value._id == value_key:
                return idx
        raise StudentDoesNotExist


class StudentDoesNotExist(Exception):
    pass
