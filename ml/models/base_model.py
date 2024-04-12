from __future__ import annotations

import abc
from src.entities import Function, ENTITY_TYPE
from configs.features_config import ExtensionFeature
import typing as tp


class BaseModel(abc.ABC):
    def __init__(self, model_name: str, model_description: str):
        self.model_name: str = model_name
        self.model_description = model_description

    def get_method_for_extension_feature(self, feature: ExtensionFeature) -> tp.Callable[[ENTITY_TYPE], str]:
        """return method for solving particular extension feature
        for example, if feature is docstring_generation,
        then method must return self.generate_docstring"""
        if feature == ExtensionFeature.docstring_generation:
            return self.generate_docstring

    @abc.abstractmethod
    def predict(self, prompt: str, *args, **kwargs) -> str:
        """return the predicted text after the given prompt"""

    @abc.abstractmethod
    def get_prompt_for_docstring_generation(self, function: Function) -> str:
        """get prompt used for docstring generation"""

    @abc.abstractmethod
    def generate_docstring(self, function: Function) -> str:
        """get docstring for the given function"""
