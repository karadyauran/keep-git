import yaml
from app.models.config_model import ConfigModel


def load_config() -> ConfigModel:
    with open("config/config.yaml", "r") as file:
        config_data = yaml.safe_load(file)
    return ConfigModel(
        openai_api_key=config_data["keys"]["openai-key"],
        generated_files_path=config_data["paths"]["output_path"],
        model_name=config_data["chat_gpt"]["model"],
        max_tokens=config_data["chat_gpt"]["max_tokens"],
        temperature=config_data["chat_gpt"]["temperature"]
    )
