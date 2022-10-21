from models.abstract import AbstractModel, ElementDoesNotExist


class Department(AbstractModel):
    COLLECTION_NAME = "departments"
    name = None
    description = None

    def __init__(self, _id, name, description):
        super().__init__(_id)
        self.name = name
        self.description = description

    def prepare_to_save(self):
        return {
            "name": self.name,
            "description": self.description
        }

    def to_json(self):
        return self.__dict__

    @staticmethod
    def create(doc):
        return Department(
            name=doc["name"],
            description=doc["description"],
            _id=str(doc["_id"]) if doc.get("_id") else None,
        )


class DepartmentDoesNotExist(ElementDoesNotExist):
    pass
