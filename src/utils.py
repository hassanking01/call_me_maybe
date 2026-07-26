from enum import Enum
from pydantic import BaseModel


class ParamType(Enum):
    NUMBER = "number"
    INTEGER = "integer"
    STRING = "string"
    BOOLEAN = "boolean"


class Function(BaseModel):
    name: str
    description: str
    parameters: dict[str, ParamType]
