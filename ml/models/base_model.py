import abc
from datasets.entities import Function, ModelDocstringResult
import typing as tp


class BaseModel(abc.ABC):
    def __init__(self, model_name: str, model_description: str, *args, **kwargs):
        self.model_name: str = model_name
        self.model_description = model_description

    @abc.abstractmethod
    def predict(self, prompt: str, *args, **kwargs) -> str:
        """just return the predicted text after the given prompt"""

    @abc.abstractmethod
    def get_prompt_for_docstring_generation(self,
                                            function: tp.Union[Function, ModelDocstringResult],
                                            *args,
                                            **kwargs) -> str:
        """get prompt used for docstring generation"""

    @abc.abstractmethod
    def generate_docstring(self,
                           function: tp.Union[Function, ModelDocstringResult],
                           *args,
                           **kwargs) -> str:
        """get docstring for the given function"""
