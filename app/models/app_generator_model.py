from enum import Enum


class Role(Enum):
    System = "system"
    User = "user"
    Assistant = "assistant"


class ChatHistory:
    role: Role
    content: str
