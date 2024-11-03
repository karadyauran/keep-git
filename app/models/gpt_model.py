from dataclasses import dataclass


@dataclass
class PromptModel:
    prompt_text: str
    max_tokens: int
    temperature: float
    model_name: str = "text-davinci-004"
