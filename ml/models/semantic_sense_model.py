from textwrap import dedent
import torch

from configs import local_model_settings as model_configs
from configs import prompts
from models import base_model as base_model_module
from src import database_entities


class DocstringModel(base_model_module.BaseModel):
    def __init__(
            self,
            model_name: str,
            model_description: str,
            prompt: str = prompts.SEMANTIC_SENSE_PROMPT,
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

    def _get_prompt(
            self,
            data_row: database_entities.SemanticSense,
    ) -> str:
        context = (
            f"\nHere you can see context of"
            f" usages of variable '{data_row.variable_name}':\n"
            f"{data_row.context[:model_configs.CONTEXT_MAX_LENGTH]}"
        )
        full_prompt = dedent(f'''
        {self._prompt}
        {context}
        Semantic sense for variable:''')

        return full_prompt
