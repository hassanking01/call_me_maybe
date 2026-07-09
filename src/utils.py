from pydantic import BaseModel
from enum import Enum

class paramType(Enum):
    NUMBER = "number"
    INTEGER = "integer"
    STRING = "string"

class Function(BaseModel):
    name: str
    description: str
    parameters: dict[str, paramType]