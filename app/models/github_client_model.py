from dataclasses import dataclass


@dataclass
class GitHubClientModel:
    github_token: dict
    repos: list
