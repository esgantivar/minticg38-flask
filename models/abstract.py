from abc import ABCMeta, abstractmethod

from bson import ObjectId


class AbstractModel(metaclass=ABCMeta):
    _id = None
    COLLECTION_NAME = ""

    def __init__(self, _id=None):
        """
        Crear el modelo
        """
        self._id = _id

    @abstractmethod
    def prepare_to_save(self):
        pass

    @abstractmethod
    def to_json(self):
        pass

    @staticmethod
    def factory(doc):
        raise NotImplemented

    @property
    def object_id(self) -> ObjectId:
        assert self._id
        return ObjectId(self._id)

    @property
    def is_new(self) -> bool:
        return not self._id


class ItemDoesNotExist(Exception):
    pass
