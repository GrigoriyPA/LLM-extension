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
            prompt: str = prompts.TEST_GENERATION_PROMPT,
            device: torch.device = model_configs.DEVICE,
            weight_type: torch.dtype = model_configs.WEIGHT_TYPE,
    ):
        super().__init__(
            model_name=model_name,
            model_description=model_description,
            device=device,
            weight_type=weight_type
        )
        self._prompt = prompt

    def _get_final_result(self, model_response: str) -> str:
        return model_response

    def _get_prompt(
            self,
            function: database_entities.Function,
    ) -> str:
        context = (
            f"\nHere you can see examples of"
            f" usages of such function:\n"
            f"{function.context[:model_configs.CONTEXT_MAX_LENGTH]}"
            if function.context else ""
        )
        full_prompt = dedent(f'''
        {self._prompt}
        {function.code}{context}
        Unit test for that function:''')

        return full_prompt
