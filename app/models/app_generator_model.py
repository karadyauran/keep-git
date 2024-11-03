from enum import Enum
from pydantic import BaseModel



class Role(Enum):
    System = "system"
    User = "user"
    Assistant = "assistant"


class ChatRecord(BaseModel):
    role: Role
    content: str
