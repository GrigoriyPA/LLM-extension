from textwrap import dedent
import torch

from configs import local_model_settings as model_configs
from configs import prompts
from models import base_model as base_model_module
from src import database_entities


class SemanticSenseModel(base_model_module.BaseModel):
    def __init__(
            self,
            model_name: str,
            model_description: str,
            model_type: str = "semantic_sense",
            prompt: str = prompts.SEMANTIC_SENSE_PROMPT,
            prompt_desc: str = "",
            device: torch.device = model_configs.DEVICE,
            weight_type: torch.dtype = model_configs.WEIGHT_TYPE,
    ):
        super().__init__(
            model_name=model_name,
            model_type=model_type,
            model_description=model_description,
            prompt=prompt,
            prompt_desc=prompt_desc,
        )
        self.device = device
        self.weight_type = weight_type

    def _get_final_result(self, model_response: str) -> str:
        return model_response

    def get_prompt(
            self,
            data_row: database_entities.SemanticSense,
    ) -> str:
        full_prompt = self.prompt.format(variable_name=data_row.variable_name, context=data_row.context)
        return full_prompt
