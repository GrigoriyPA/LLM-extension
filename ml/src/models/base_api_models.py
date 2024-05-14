from __future__ import annotations

import abc
from src.scorers import score_function
import asyncio
from src.models import base_models as base_models_module


class BaseApiModel(base_models_module.BaseModel, abc.ABC):
    def __init__(
            self,
            model_name: str,
            model_type: str,
            model_description: str,
            prompt: str,
            prompt_desc: str = "",
    ):
        super().__init__(
            model_name=model_name,
            model_type=model_type,
            model_description=model_description,
            prompt=prompt,
            prompt_desc=prompt_desc,
        )
        self._model = score_function.GenerativeModel()

    def _predict(
            self,
            prompt: str,
            **generation_kwargs,
    ) -> str:
        return asyncio.run(self._model.get_model_response(prompt, False))

    def clear_model(self) -> None:
        pass
