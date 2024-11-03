from app.models.config_model import ConfigModel
from app.models.respoces.app_idea_responce import AppResponse
from openai import OpenAI, ChatCompletion

from app.models.app_generator_model import Role, ChatRecord


class AppGenerator:
    def __init__(self, cfg: ConfigModel) -> None:
        self.cfg = cfg
        self.client = OpenAI(api_key=cfg.openai_api_key)
        self.history = []

    def send_request(self, request: str, response_format, model: str = None, temperature: float = None, max_tokens: int = 1000):
        messages = self.history + [
            {
                "role": "user",
                "content": request
            }
        ]

        model = model or self.cfg.model_name
        temperature = temperature if temperature is not None else self.cfg.temperature

        responce: ChatCompletion = self.client.beta.chat.completions.parse(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format=response_format
        )
        ans = responce.choices[0].message

        self.save_history(ChatRecord(
            role=Role.User,
            content=request
        ))

        self.save_history(ChatRecord(
            role=Role.Assistant,
            content=ans.content
        ))

        return ans.parsed

    def save_history(self, chat_record: ChatRecord) -> None:
        self.history.append(
            {
                "role": chat_record.role.value,
                "content": chat_record.content
            }
        )
    