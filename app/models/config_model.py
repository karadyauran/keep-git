from dataclasses import dataclass


@dataclass
class ConfigModel:
    openai_api_key: str
    generated_files_path: str
    model_name: str
    max_tokens: int
    temperature: float
