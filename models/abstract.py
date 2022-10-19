from abc import ABCMeta


class AbstractModel(metaclass=ABCMeta):
    _id = None
    COLLECTION_NAME = ""

    def __init__(self, _id=None):
        """
        Crear el modelo
        """
        self._id = _id


