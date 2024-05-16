import abc
import re
import torch

from configs import local_model_settings as model_configs
from configs import prompts
from src.models import base_models as base_models_module
from src.models import base_api_models as base_api_models
from src.database import database_entities


class TestGenerationModel(base_models_module.BaseModel, abc.ABC):
    def _get_final_result(self, model_response: str) -> str:
        regexp_result = re.search('```(?:python)?(.*?)```', model_response,
                                  re.DOTALL)
        return regexp_result.group(1) if regexp_result else model_response

    def get_prompt(
            self,
            data_row: database_entities.UnitTest,
    ) -> str:
        full_prompt = self.prompt.format(code=data_row.code)
        return full_prompt


class TestGenerationApiModel(
    base_api_models.BaseApiModel, TestGenerationModel
):
    def __init__(
            self,
            model_name: str = "synthetic",
            model_type: str = "test_generation",
            model_description: str = "llama70b api",
            prompt: str = prompts.TEST_GENERATION_PROMPT,
            prompt_desc: str = "",
    ):
        super().__init__(
            model_name=model_name,
            model_type=model_type,
            model_description=model_description,
            prompt=prompt,
            prompt_desc=prompt_desc,
        )


class TestGenerationLocalModel(
    base_models_module.BaseLocalModel,
    TestGenerationModel
):
    def __init__(
            self,
            model_name: str,
            model_description: str,
            model_type: str = 'test_generation',
            prompt: str = prompts.TEST_GENERATION_PROMPT,
            prompt_desc: str = "",
            device: torch.device = model_configs.DEVICE,
            weight_type: torch.dtype = model_configs.WEIGHT_TYPE,
    ):
        super().__init__(
            model_name=model_name,
            model_type=model_type,
            model_description=model_description,
            device=device,
            weight_type=weight_type,
            prompt=prompt,
            prompt_desc=prompt_desc,
        )
