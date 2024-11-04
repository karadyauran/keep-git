from pydantic import BaseModel

class File(BaseModel):
    path: str
    filename: str

class StructureResponse(BaseModel):
    file: list[File]
