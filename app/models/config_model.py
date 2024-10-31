from dataclasses import dataclass

@dataclass
class ConfigModel:
    generated_files_path: str
    model_name: str
    max_tokens: int
    temperature: float