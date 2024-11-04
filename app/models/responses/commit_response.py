from pydantic import BaseModel


class CommitResponse(BaseModel):
    commit: str
