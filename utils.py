from typing import Optional

from bson import ObjectId


def parse_object_id(object_id: Optional[ObjectId]) -> Optional[str]:
    return str(object_id) if object_id else None
