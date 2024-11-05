import os
from github import Github, GithubException

from app.models.github_client_model import GitHubClientModel


class GitHubService:
    def __init__(self, github_cfg: GitHubClientModel):
        self.github_cfg = github_cfg
        self.g = Github(self.github_cfg.github_token)
        self.repo = self.g.get_repo(self.github_cfg.repo)
        self.branch = "main"

    def upload_file(self, local_file_path: str, commit_message: str, remote_dir="") -> None:
        relative_path = os.path.basename(local_file_path)
        remote_file_path = os.path.join(remote_dir, relative_path).replace("\\", "/")

        with open(local_file_path, "r") as file:
            content = file.read()

        try:
            self.repo.create_file(
                path=remote_file_path,
                message=commit_message,
                content=content,
                branch=self.branch
            )
        except Exception as e:
            print(f"Failed to upload {remote_file_path}: {e}")

    def delete_all_files(self):
        try:
            contents = self.repo.get_contents("", ref=self.branch)

            if not contents:
                print("Repository is empty. Nothing to delete.")
                return

            files_to_delete = []

            while contents:
                file_content = contents.pop(0)
                if file_content.type == "dir":
                    contents.extend(self.repo.get_contents(file_content.path, ref=self.branch))
                else:
                    files_to_delete.append(file_content)

            for file_content in files_to_delete:
                self.repo.delete_file(
                    path=file_content.path,
                    message=f"Deleted file {file_content.path}",
                    sha=file_content.sha,
                    branch=self.branch
                )
        except GithubException as e:
            if e.status == 404:
                print("Repository is empty. Nothing to delete.")
            else:
                print(f"An error occurred: {e}")
