from app.models import ConfigModel, GitHubClientModel
from app.service import AppGenerator, GitHubService


class Service:
    def __init__(self, cfg: ConfigModel, github_client: GitHubClientModel):
        self.GitHubService = GitHubService(github_client)
        self.AppGenerator = AppGenerator(cfg, self.GitHubService)
