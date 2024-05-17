import abc
import torch
import typing as tp
import transformers

from configs import local_model_settings as model_configs
from configs import prompts
from src.models import base_models as base_models_module
from src.database import database_entities


class BaseAutoCompleteModel(base_models_module.BaseModel, abc.ABC):
    def _get_final_result(self, model_response: str) -> str:
        return model_response

    def get_prompt(
            self,
            data_row: database_entities.AutoComplete,
    ) -> str:
        full_prompt = self.prompt.format(code=data_row.code)
        return full_prompt


class AutoCompleteLocalModel(
    base_models_module.BaseLocalModel,
    BaseAutoCompleteModel
):
    def __init__(
        self,
        model_name: str,
        model_description: str,
        model_type: str = "autocomplete",
        prompt: str = prompts.EMPTY_AUTOCOMPLETE_PROMPT,
        prompt_desc: str = "",
        device: torch.device = model_configs.DEVICE,
        weight_type: torch.dtype = model_configs.WEIGHT_TYPE,
        generation_config: tp.Optional[transformers.GenerationConfig] = None,
    ):
        super().__init__(
            model_name=model_name,
            model_type=model_type,
            model_description=model_description,
            prompt=prompt,
            prompt_desc=prompt_desc,
            generation_config=generation_config,
        )
        self.device = device
        self.weight_type = weight_type
