from textwrap import dedent
import torch

from configs import local_model_settings as model_configs
from configs import prompts
from models import base_model as base_model_module
from src import database_entities


class TestGenerationModel(base_model_module.BaseModel):
    def __init__(
            self,
            model_name: str,
            model_description: str,
            model_type: str = 'test_generation',
            prompt: str = prompts.TEST_GENERATION_PROMPT,
            device: torch.device = model_configs.DEVICE,
            weight_type: torch.dtype = model_configs.WEIGHT_TYPE,
    ):
        super().__init__(
            model_name=model_name,
            model_type=model_type,
            model_description=model_description,
            device=device,
            weight_type=weight_type,
            prompt=prompt
        )
        self.prompt = prompt

    def _get_final_result(self, model_response: str) -> str:
        return model_response

    def get_prompt(
            self,
            unittest: database_entities.UnitTest,
    ) -> str:
        full_prompt = self.prompt.format(code=unittest.code)
        return full_prompt
