import os

import yaml
from dotenv import load_dotenv
from app.models import ConfigModel, PromptsModel, GitHubClientModel


def load_config_model() -> ConfigModel:
    load_dotenv()

    with open("config/config.yaml", "r") as file:
        config_data = yaml.safe_load(file)
    return ConfigModel(
        openai_api_key=os.getenv(config_data["keys"]["openai-key"]),
        generated_files_path=config_data["paths"]["output_path"],
        model_name=config_data["chat_gpt"]["model"],
        max_tokens=config_data["chat_gpt"]["max_tokens"],
        temperature=config_data["chat_gpt"]["temperature"]
    )


def load_prompts() -> PromptsModel:
    with open("config/prompts.yaml", "r") as file:
        config_data = yaml.safe_load(file)
    return PromptsModel(
        default_settings={
            "role": config_data["defaults"]["settings"]["role"],
            "code_style": config_data["defaults"]["settings"]["code_style"],
        },
        idea_prompt=config_data["prompts"]["idea"]["prompt"],
        structure_prompt=config_data["prompts"]["structure"]["prompt"],
        code_prompt=config_data["prompts"]["code"]["prompt"],
        commit_prompt=config_data["prompts"]["commit"]["prompt"],
    )


def load_github_config() -> GitHubClientModel:
    with open("config/github.yaml", "r") as file:
        config_data = yaml.safe_load(file)
    return GitHubClientModel(
        github_token=os.getenv(config_data["tokens"]["github_token"]),
        repo=os.getenv(config_data["repo"]),
    )
