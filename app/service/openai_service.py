from openai import OpenAI
from openai.types.chat import ParsedChatCompletion

from app.domain.openai_domain import OpenaiRequest


class OpenAIService:
    def __init__(self, open_ai_token: str):
        self.openai: OpenAI = OpenAI(api_key=open_ai_token)
        self.messages: list[dict[str:str]] = []

    def openai_normal_request(self, request: OpenaiRequest) -> ParsedChatCompletion:
        self._save_user_messages(request.message)

        answer: request.response = self.openai.beta.chat.completions.parse(
            messages=self.messages,
            model=request.model,
            response_format=request.response
        ).choices[0].message

        self._save_assistant_messages(answer.content)
        return answer.parsed

    def openai_request_with_no_answer(self, request: OpenaiRequest) -> None:
        self._save_user_messages(request.message)

        answer: str = self.openai.chat.completions.create(
            messages=self.messages,
            model=request.model,
            response_format=request.response
        ).choices[0].message.content

        self._save_assistant_messages(answer)

    def _save_user_messages(self, user_content: str) -> None:
        self.messages.append({
            "role": "user",
            "content": user_content
        })

    def _save_assistant_messages(self, assistant_content: str) -> None:
        self.messages.append({
            "role": "assistant",
            "content": assistant_content
        })
