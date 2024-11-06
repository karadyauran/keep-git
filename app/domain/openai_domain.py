import app.domain.responses_domain as responses_domain

class OpenaiRequest:
    def __init__(
            self,
            message: str,
            response: responses_domain = None,
            max_token: int = 16000,
    ) -> None:
        self.message = message
        self.response = response
        self.max_token = max_token

        self.model = "gpt-4o"

    def __str__(self) -> str:
        return self.message
