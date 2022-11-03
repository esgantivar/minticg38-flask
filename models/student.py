from models.abstract import AbstractModel, ElementDoesNotExist


class Student(AbstractModel):
    COLLECTION_NAME = "students"

    cedula = None
    first_name = None
    last_name = None
    email = None
    auth_id: str = None

    def __init__(
            self,
            cedula,
            first_name,
            last_name,
            email,
            auth_id=None,
            _id=None,
    ):
        super().__init__(_id)
        self.cedula = cedula
        self.last_name = last_name
        self.first_name = first_name
        self.email = email
        self.auth_id = auth_id

    def prepare_to_save(self):
        return {
            "cedula": self.cedula,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "auth_id": self.auth_id
        }

    def to_json(self):
        return self.__dict__

    @staticmethod
    def create(doc):
        """
        Patron Factory
        """
        return Student(
            cedula=doc["cedula"],
            last_name=doc["last_name"],
            first_name=doc["first_name"],
            email=doc["email"],
            auth_id=doc.get("auth_id") if doc.get("auth_id") else None,
            _id=str(doc["_id"]) if doc.get("_id") else None,
        )


class StudentDoesNotExist(ElementDoesNotExist):
    pass
