import os

import yaml
from dotenv import load_dotenv

class Config:
    def __init__(self, config_path='app/config/config.yaml'):
        load_dotenv()
        with open(config_path, "r") as file:
            config_data = yaml.safe_load(file)

        self.paths: dict = config_data['paths']
        self.tokens: dict = config_data["tokens"]
        self.prompts: dict = config_data["prompts"]

        self.tokens["openai_token"] = os.getenv("OPENAI_TOKEN")
        self.tokens["github"]["token"] = os.getenv("GITHUB_TOKEN")
