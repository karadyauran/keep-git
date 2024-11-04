import os
import shutil

from openai import OpenAI
from openai.types.chat.parsed_chat_completion import ParsedChatCompletion

from app.core.load_config import load_config_model, load_prompts, load_github_config
from app.models.config_model import ConfigModel
from app.models.prompts_model import PromptsModel
import app.models.responses as responses
from app.models.app_generator_model import Role, ChatRecord
from app.models.responses import AppResponse, StructureResponse, CodeResponse, CommitResponse

from app.service.github_service import GitHubService


def create_file_with_code(file_path, file_name, code) -> None:
    """Creates files"""
    os.makedirs(file_path, exist_ok=True)
    with open(file_path + file_name, mode='w') as file:
        file.write(code)
        file.close()

def reset_folder(folder_path: str) -> None:
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.mkdir(folder_path)


class AppGenerator:
    def __init__(self, cfg: ConfigModel, github_service: GitHubService) -> None:
        self.cfg = cfg
        self.client = OpenAI(api_key=cfg.openai_api_key)
        self.history = []

        self.github_service = github_service

    def send_request(self, request: str, response_format: responses, model: str = None, temperature: float = None,
                     max_tokens: int = 1000) -> ParsedChatCompletion:
        self.save_history(ChatRecord(
            role=Role.User,
            content=request
        ))

        model = model or self.cfg.model_name
        temperature = temperature if temperature is not None else self.cfg.temperature

        response: ParsedChatCompletion = self.client.beta.chat.completions.parse(
            messages=self.history,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format=response_format
        )
        ans = response.choices[0].message

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

    def create_app(self) -> None:
        """Creates an application"""
        self.github_service.delete_all_files()

        prompts: PromptsModel = load_prompts()  # import prompts from prompts config

        # Idea generator
        idea: AppResponse = self.send_request(request=prompts.idea_prompt, response_format=responses.AppResponse,
                                              max_tokens=100)

        project_path = self.cfg.generated_files_path + idea.name_of_project + "/"

        structure: StructureResponse = self.send_request(request=prompts.structure_prompt,
                                                         response_format=responses.StructureResponse, max_tokens=500)

        for file in structure.file:
            file_path = file.path + file.filename

            code: CodeResponse = self.send_request(request=prompts.code_prompt.format(file_path=file_path),
                                                   response_format=responses.CodeResponse,
                                                   max_tokens=self.cfg.max_tokens)

            file_path = project_path + file.path
            create_file_with_code(file_path=file_path, file_name=file.filename, code=code.code)

            commit_message: CommitResponse = self.send_request(request=prompts.commit_prompt,
                                                               response_format=CommitResponse,
                                                               max_tokens=100)

            self.github_service.upload_file(local_file_path=file_path+file.filename, commit_message=commit_message.commit,
                                            remote_dir=file.path)

        reset_folder(self.cfg.generated_files_path)
