from pydantic import BaseModel


class File(BaseModel):
    path: str
    name: str

    def __str__(self) -> str:
        return f"{self.path}{self.name}"


class StructureResponse(BaseModel):
    file: list[File]


class CodeResponse(BaseModel):
    code: str


class CommitResponse(BaseModel):
    commit_message: str
