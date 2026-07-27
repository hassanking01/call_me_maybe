from enum import Enum
from pydantic import BaseModel


class ParamType(Enum):
    """Supported parameter types for functions."""

    NUMBER = "number"
    INTEGER = "integer"
    STRING = "string"
    BOOLEAN = "boolean"


class Function(BaseModel):
    """Data model for function definitions.

    Attributes:
        name: Name of the function.
        description: Description of the function purpose.
        parameters: Mapping of parameter names to their types.
    """

    name: str
    description: str
    parameters: dict[str, ParamType]
