import app.domain.responses_domain as responses_domain
import app.utils as utils

from app.service.openai_service import OpenAIService
from app.domain.openai_domain import OpenaiRequest

from tqdm import tqdm


class AppGeneratorService:
    def __init__(self, openai_service: OpenAIService, prompts: dict) -> None:
        self._openai_service: OpenAIService = openai_service
        self.prompts: dict = prompts
        self.structure = responses_domain.StructureResponse

    def generate_tmp_project(self) -> None:
        self.structure = responses_domain.StructureResponse

        # Initialize progress bar for each step
        with tqdm(total=3, desc="Generating Project", unit="step") as progress_bar:
            # Step 1: Generate idea
            self._openai_service.openai_request_with_no_answer(
                OpenaiRequest(
                    message=self.prompts["idea"]["prompt"],
                    max_token=50,
                )
            )
            progress_bar.update(1)  # Update progress after step completion

            # Step 2: Generate file structure for project
            self.structure = self._openai_service.openai_normal_request(
                OpenaiRequest(
                    message=self.prompts["structure"]["prompt"],
                    max_token=1500,
                    response=responses_domain.StructureResponse
                )
            )
            progress_bar.update(1)

            # Step 3: Generate content for each file
            for file in tqdm(self.structure.file, desc="Generating Files", unit="file"):
                content: responses_domain.CodeResponse = self._openai_service.openai_normal_request(
                    OpenaiRequest(
                        message=self.prompts["code"]["prompt"].format(file_path=file.__str__()),
                        response=responses_domain.CodeResponse
                    )
                )

                tmp_file_path = "output/" + file.path
                utils.create_file_with_content(
                    file_path=tmp_file_path,
                    file_name=file.name,
                    content=content.code
                )
            progress_bar.update(1)
