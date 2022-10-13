from models.abstract import AbstractModel


class Student(AbstractModel):
    cedula = None
    first_name = None
    last_name = None
    email = None

    def __init__(
        self,
        _id,
        cedula,
        first_name,
        last_name,
        email,
    ):
        super().__init__(_id)
        self.cedula = cedula
        self.last_name = last_name
        self.first_name = first_name
        self.email = email
