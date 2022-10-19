from models.abstract import AbstractModel, ItemDoesNotExist
from utils import parse_object_id


class Department(AbstractModel):
    COLLECTION_NAME = "deparments"

    name = None
    description = None

    def __init__(self, name, description, _id=None):
        super().__init__(_id)
        self.name = name
        self.description = description

    def prepare_to_save(self):
        return {
            "name": self.name,
            "description": self.description
        }

    @staticmethod
    def factory(doc):
        return Department(
            name=doc["name"],
            description=doc["description"],
            _id=parse_object_id(doc["_id"]),
        )

    def to_json(self):
        return self.__dict__


class DepartmentDoesNotExist(ItemDoesNotExist):
    pass
