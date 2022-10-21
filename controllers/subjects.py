from controllers.abstract import CRUDController
from models.deparment import Department, DepartmentDoesNotExist
from models.subject import Subject, SubjectDoesNotExist
from repositories.department import DepartmentRepository
from repositories.subject import SubjectRepository


class SubjectsController(CRUDController):
    def __init__(self):
        self.repository = SubjectRepository(
            Subject,
            SubjectDoesNotExist
        )
        self.repo_d = DepartmentRepository(
            Department,
            DepartmentDoesNotExist
        )

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id_element):
        return self.repository.get_by_id(id_element)

    def create(self, content):
        doc_department = content.get("department", {})
        department = self.repo_d.get_by_id(doc_department.get("id"))
        content["department"] = department.to_json()
        return self.repository.save(
            item=Subject.create(content)
        )

    def update(self, id_element, content):
        element = self.get_by_id(id_element)
        element.name = content["name"]
        element.course_credits = content["course_credits"]
        return self.repository.save(element)

    def delete(self, id_element):
        element = self.get_by_id(id_element)
        return self.repository.delete(element)

    def count(self):
        return self.repository.count()

    def set_department_to_subject(self, id_subject, id_department):
        subject = self.repository.get_by_id(id_subject)
        department = self.repo_d.get_by_id(id_department)
        subject.department = department
        return self.repository.save(subject)


