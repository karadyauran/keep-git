from pydantic import BaseModel


class AppResponce(BaseModel):
    name_of_project: str
    small_description: str
