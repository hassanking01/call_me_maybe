from pydantic import BaseModel
class prompt(BaseModel):
    prompt: str

class parameter(BaseModel):
    name: str
    type: str | int | float
class function(BaseModel):
    name: str
    description: str
