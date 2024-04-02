import g4f
import typing as tp
import re

from .models_names import GPTModelName, GPTProviderName

from .consts import SCORE_FUNCTION, PROMPTS

from datasets.entities import Function, ModelDocstringResult
from datasets.database_utils import Dataset, get_tmp_dataset


class SessionInfo:
    def __init__(self, max_length: int = 4096):
        self.history: tp.List[tp.Dict[str, str]] = []
        self.max_length: int = max_length
        self.current_length: int = 0

    def trim_history(self) -> None:
        while len(self.history) > 1 and self.current_length > self.max_length:
            removed_message = self.history.pop(0)
            self.current_length -= len(removed_message["content"])

    def add_content(self, action: tp.Dict[str, str]):
        self.history.append(action)
        self.current_length += len(action["content"]) if action['content'] is not None else 0
        self.trim_history()

    def get_history(self) -> tp.List[tp.Dict[str, str]]:
        return self.history


class GenerativeModel:
    def __init__(
            self,
            model: tp.Union[g4f.models.Model, str] = getattr(g4f.models,
                                                             GPTModelName[SCORE_FUNCTION["model_name"]].value),
            provider: tp.Union[g4f.providers.types.ProviderType, str, None] = getattr(g4f.Provider, GPTProviderName[
                SCORE_FUNCTION["provider_name"]].value)
    ):
        self.__chat_completion = g4f.ChatCompletion
        self.__model = model
        self.__provider = provider

    async def get_answer(
            self, history: tp.List[tp.Dict[str, str]]
    ) -> str:
        return await self.__chat_completion.create_async(
            model=self.__model,
            messages=history,
            provider=self.__provider
        )

    def get_provider_name(self):
        return self.__provider.__name__


class ScoreFunction:
    def __init__(
            self,
            prompt: str = PROMPTS[0],
            model: GenerativeModel = GenerativeModel()
    ):
        self.__session_info: SessionInfo = SessionInfo()
        self.__model: GenerativeModel = model
        self.__prompt: str = prompt

    def prepare_prompt(self, function: Function) -> str:
        return self.__prompt.format(docstring=function.docstring, function_code=function.code)

    async def get_model_response(
            self,
            user_input: str,
            use_history: bool,
    ) -> str:
        content = {"role": "user", "content": user_input}
        self.__session_info.add_content(content)
        try:
            history = self.__session_info.get_history() \
                if use_history else [content]
            model_response = await self.__model.get_answer(history)
        except Exception as e:
            print(f"{self.__model.get_provider_name()}:", e)
            model_response = None

        self.__session_info.add_content({"role": "assistant", "content": model_response})
        return model_response

    @staticmethod
    def extract_score(answer: str) -> tp.Optional[float]:
        if answer is None:
            return None
        numbers = re.findall(r"[-+]?\d*\.\d+|\d+", answer)
        if not numbers:
            return None
        return float(numbers[-1])

    async def exec_one(self, function: Function, use_history: bool = False) -> ModelDocstringResult:
        text = self.prepare_prompt(function)
        output = await self.get_model_response(
            user_input=text,
            use_history=use_history,
        )
        score = self.extract_score(output)

        result = ModelDocstringResult(
            **function._asdict(),
            model_name="",  # shall be overwritten in the outer code
            prompt="",  # shall be overwritten in the outer code
            scorer_prompt=text,
            docstring_score=score,
            scorer_response=output,
        )

        return result

    async def exec(self, src: Dataset, dst: tp.Optional[Dataset] = None, use_history: bool = False) -> Dataset:
        """
        Scores every function in src dataset and writes result to dst dataset
        :param src: Dataset of Function elements
        :param dst: Dataset of ModelDocstringResult elements, if not passed then tmp table will be created and returned
        :param use_history:
        """
        if not dst:
            dst = get_tmp_dataset(ModelDocstringResult)
        for function in src.read():
            dst.write(await self.exec_one(function, use_history))
        return dst

    def update_prompt(self, prompt: str):
        self.__prompt = prompt
