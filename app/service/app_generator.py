from app.models.config_model import ConfigModel
from app.models.respoces.app_idea_responce import AppResponce
from openai import OpenAI, ChatCompletion

from app.models.app_generator_model import Role, ChatHistory


class AppGenerator:
    def __init__(self, cfg: ConfigModel) -> None:
        self.cfg = cfg
        self.client = OpenAI(api_key=cfg.openai_api_key)
        self.history = []

    def send_request(self, request: str, responce_format, model: str = "", temperature: int = 0, max_tokens: int = 1000):
        responce: ChatCompletion = self.client.beta.chat.completions.parse(
            messages=[
                {
                    "role": "user",
                    "content": request
                }
            ],
            model=self.cfg.model_name if model == "" else model,
            temperature=self.cfg.temperature if temperature == 0 else temperature,
            max_tokens=max_tokens,
            response_format=responce_format
        )

        ans = responce.choices[0].message
        return ans

    def save_history(self, role: Role, content: str) -> None:
        self.history.append(ChatCompletion(role=role, content=content))
