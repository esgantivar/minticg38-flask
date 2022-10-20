from controllers.abstract import CRUDController
from models.subject import Subject, SubjectDoesNotExist
from repositories.subject import SubjectRepository


class SubjectsController(CRUDController):

    def __init__(self):
        self.repo = SubjectRepository(
            model=Subject,
            exception=SubjectDoesNotExist
        )

    def get_all(self):
        return self.repo.get_all()

    def get_by_id(self, id_element):
        return self.repo.get_by_id(id_element)

    def create(self, content):
        return self.repo.save(
            item=Subject.factory(content)
        )

    def update(self, id_element, content):
        element = self.get_by_id(id_element)
        element.name = content["name"]
        element.description = content["description"]
        return self.repo.save(element)

    def delete(self, id_element):
        element = self.get_by_id(id_element)
        return self.repo.delete(element)

    def count(self):
        return self.repo.count()
