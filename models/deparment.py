from models.abstract import AbstractModel


class Department(AbstractModel):
    name = None
    description = None

    def __init__(self, _id, name, description):
        super().__init__(_id)
        self.name = name
        self.description = description
