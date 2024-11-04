from dataclasses import dataclass


@dataclass
class PromptsModel:
    defalut_settings: dict
    idea_prompt: str
    structure_prompt: str
    code_prompt: str
    commit_prompt: str
