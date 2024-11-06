from os import path

from github import Github, Repository, InputGitTreeElement

from app.service import OpenAIService, OpenaiRequest
from app.utils.file_utils import reset_folder
from app.domain.responses_domain import StructureResponse, CommitResponse

from tqdm import tqdm


class GithubService:
    def __init__(self, openai_service: OpenAIService, github_token: str, repo: str, structure: StructureResponse,
                 commit_prompt: str):
        self._openai_service: OpenAIService = openai_service
        self.github: Github = Github(github_token)
        self.repo: Repository = self.github.get_repo(repo)

        self.structure: StructureResponse = structure
        self.commit_prompt: str = commit_prompt

        self.branch: str = 'main'

    def _upload_file(self, local_file_path: str, remote_file_path: str, commit_message: str) -> None:
        relative_path = path.basename(local_file_path)
        remote_file_path = path.join(remote_file_path, relative_path).replace("\\", "/")

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

    def _delete_all_files_and_add_real_file(self, commit_message: str = "Delete all files and add README",
                                            file_path: str = "output/README.md") -> None:
        if not path.isfile(file_path):
            print(f"File '{file_path}' does not exist.")
            return

        with open(file_path, 'r') as f:
            file_content = f.read()

        main_ref = self.repo.get_git_ref("heads/main")
        latest_commit = self.repo.get_commit(main_ref.object.sha)

        new_file = InputGitTreeElement(
            path="README.md",
            mode="100644",
            type="blob",
            content=file_content
        )
        new_tree = self.repo.create_git_tree([new_file])
        new_commit = self.repo.create_git_commit(commit_message, new_tree, [latest_commit.commit])
        main_ref.edit(new_commit.sha)

    def _upload_to_github(self) -> None:
        for file in tqdm(self.structure.file, desc="Upload files", unit="file"):
            if file.name != "README.md":
                commit: str = self._openai_service.openai_normal_request(
                    OpenaiRequest(
                        message=self.commit_prompt,
                        max_token=100,
                        response=CommitResponse
                    )
                ).commit_message

                self._upload_file(
                    local_file_path="output/" + file.__str__(),
                    remote_file_path=file.path,
                    commit_message=commit
                )

    def upload_project_on_github(self) -> None:
        with tqdm(total=3, desc="Uploading on GitHub", unit="step") as progress_bar:
            progress_bar.update(1)
            self._delete_all_files_and_add_real_file()

            progress_bar.update(1)
            self._upload_to_github()

            progress_bar.update(1)
            reset_folder()
