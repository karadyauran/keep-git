from app.config import Config
from app.service import OpenAIService
from app.service.app_generator_service import AppGeneratorService
from app.service.github_service import GithubService

if __name__ == '__main__':
    config = Config()

    openai_service = OpenAIService(config.tokens["openai_token"])
    app_generator_service = AppGeneratorService(openai_service=openai_service, prompts=config.prompts)

    app_generator_service.generate_tmp_project()

    github_service = GithubService(
        openai_service=openai_service,
        github_token=config.tokens["github"]["token"],
        repo=config.tokens["github"]["repo"],
        structure=app_generator_service.structure,
        commit_prompt=config.prompts["commit"]["prompt"],
    )

    github_service.upload_project_on_github()
