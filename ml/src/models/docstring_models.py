import abc
import re
import torch
import typing as tp

from configs import local_model_settings as model_configs
from configs import prompts
from src.database import database_entities
from src.models import base_models as base_models_module
from src.models import base_api_models as base_api_models_module


class BaseDocstringModel(base_models_module.BaseModel, abc.ABC):
    def _get_final_result(self, model_response: str) -> str:
        regexp_result = re.search(
            '([\'\"]{3})(.*?)([\'\"]{3})', model_response, re.DOTALL
        )
        return regexp_result.group(2) if regexp_result else model_response

    def get_prompt(
            self,
            data_row: database_entities.Function,
    ) -> str:
        context = (
            f"\nHere you can see examples of"
            f" usages of such function:"
            f"\n{data_row.context[:model_configs.CONTEXT_MAX_LENGTH]}"
            if data_row.context else ""
        )
        full_prompt = self.prompt.format(
            code=data_row.code, context_info=context
        )
        return full_prompt


class DocstringApiModel(base_api_models_module.BaseApiModel, BaseDocstringModel):
    def __init__(
            self,
            model_name: str = "synthetic",
            model_type: str = "docstring",
            model_description: str = "llama70b api",
            prompt: str = prompts.DOCSTRING_PROMPT,
            prompt_desc: str = "",
    ):
        super().__init__(
            model_name=model_name,
            model_type=model_type,
            model_description=model_description,
            prompt=prompt,
            prompt_desc=prompt_desc,
        )


class DocstringLocalModel(
    base_models_module.BaseLocalModel,
    BaseDocstringModel
):
    def __init__(
            self,
            model_name: str,
            model_description: str,
            model_type: str = "docstring",
            prompt: str = prompts.DOCSTRING_PROMPT,
            prompt_desc: str = "",
            device: torch.device = model_configs.DEVICE,
            weight_type: torch.dtype = model_configs.WEIGHT_TYPE,
            lora_part_path: tp.Optional[str] = None,
    ):
        super().__init__(
            model_name=model_name,
            model_type=model_type,
            model_description=model_description,
            device=device,
            weight_type=weight_type,
            prompt=prompt,
            prompt_desc=prompt_desc,
            lora_part_path=lora_part_path,
        )
