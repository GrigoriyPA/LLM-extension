from textwrap import dedent
import re

from configs import local_model_settings as model_configs
from configs import prompts
from src import database_entities
from src import score_function
from models import base_model as base_model_module
import asyncio


class DocstringLLamaModel(base_model_module.BaseModel):
    def __init__(
            self,
            model_name: str = "synthetic",
            model_type: str = "docstring",
            model_description: str = "llama70b api",
            prompt: str = prompts.DOCSTRING_PROMPT
    ):
        super().__init__(
            model_name=model_name,
            model_type=model_type,
            model_description=model_description,
            prompt=prompt,
        )
        self._model = score_function.GenerativeModel()

    def _get_final_result(self, model_response: str) -> str:
        regexp_result = re.search('([\'\"]{3})(.*?)([\'\"]{3})', model_response, re.DOTALL)
        return regexp_result.group(2) if regexp_result else model_response

    def get_prompt(
            self,
            data_row: database_entities.Function,
    ) -> str:
        context = (
            f"\nHere you can see examples of"
            f" usages of such function:\n{data_row.context[:model_configs.CONTEXT_MAX_LENGTH]}"
            if data_row.context else ""
        )
        full_prompt = self.prompt.format(code=data_row.code, context_info=context)
        return full_prompt
    
    def _predict(
            self,
            prompt: str,
            **generation_kwargs,
    ) -> str:
        return asyncio.run(self._model.get_model_response(prompt, False))
    
    def _load_model(self) -> None:
        return
