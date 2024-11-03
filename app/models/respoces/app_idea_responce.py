from pydantic import BaseModel


class AppResponse(BaseModel):
    name_of_project: str
    small_description: str
