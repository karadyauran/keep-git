from dataclasses import dataclass


@dataclass
class GitHubClientModel:
    github_token: str
    repo: str
