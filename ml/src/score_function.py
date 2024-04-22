import re
import typing as tp

import g4f

from constants import score_functions as score_functions_constants
from models import base_model as base_model_module
from src import database_entities, database_utils


class SessionInfo:
    def __init__(
            self,
            max_length: int = score_functions_constants.DEFAULT_CONTEXT_LENGTH
    ):
        self.history: tp.List[tp.Dict[str, str]] = []
        self.max_length: int = max_length
        self.current_length: int = 0

    def trim_history(self) -> None:
        while len(self.history) > 1 and self.current_length > self.max_length:
            removed_message = self.history.pop(0)
            self.current_length -= len(removed_message["content"])

    def add_content(self, action: tp.Dict[str, str]) -> None:
        self.history.append(action)
        self.current_length += (
            len(action["content"]) if action['content'] is not None else 0
        )
        self.trim_history()

    def get_history(self) -> tp.List[tp.Dict[str, str]]:
        return self.history


class GenerativeModel:
    def __init__(
            self,
            model: tp.Union[g4f.models.Model, str] = getattr(
                g4f.models,
                score_functions_constants.DEFAULT_FUNCTION.value
            ),
            provider: tp.Union[g4f.providers.types.ProviderType, str, None] = (
                    getattr(
                        g4f.Provider,
                        score_functions_constants.DEFAULT_PROVIDER.value
                    )
            )
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
            prompt: str = score_functions_constants.PROMPTS[0],  # TODO
            model: GenerativeModel = GenerativeModel()
    ):
        self.__session_info: SessionInfo = SessionInfo()
        self.__model: GenerativeModel = model
        self.__prompt: str = prompt

    def prepare_prompt(self, function: database_entities.Function) -> str:
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
        match = re.search(r"Degree of correspondence: (\d+\.\d+)", answer)

        if match:
            return float(match.group(1))

        match = re.findall(r"[-+]?\d*\.\d+|\d+", answer)
        if not match:
            return None
        if float(match[-1]) < 0 or float(match[-1]) > 1:
            return None
        return float(match[-1])

    async def exec_one(
            self,
            function: database_entities.Function,
            model: base_model_module.BaseModel,
            use_history: bool = False
    ) -> database_entities.ScorerModelDocstringResult:
        text = self.prepare_prompt(function)
        output = await self.get_model_response(
            user_input=text,
            use_history=use_history,
        )
        score = self.extract_score(output)

        result = database_entities.ScorerModelDocstringResult(
            **function.__dict__,
            model_name=model.model_name,
            prompt=model.get_prompt_for_docstring_generation(function),
            scorer_prompt=text,
            docstring_score=score,
            scorer_response=output,
        )

        return result

    async def exec(
            self,
            src: database_utils.Table[database_entities.Function],
            model: base_model_module.BaseModel,
            dst: tp.Optional[
                database_utils.Table[database_entities.ScorerModelDocstringResult]
            ] = None,
            use_history: bool = False
        ) -> database_utils.Table[database_entities.ScorerModelDocstringResult]:
        """
        Scores every function in src dataset and writes result to dst dataset
        :param src: Dataset of Function elements
        :param model: Model which was used for predictions
        :param dst: Dataset of ModelDocstringResult elements,
        if not passed then tmp table will be created and returned
        :param use_history:
        """
        if not dst:
            dst = database_utils.create_new_table(
                row_type=database_entities.ScorerModelDocstringResult,
                table_name=f'scorer_{model.model_name}_results'
            )
        for row in src.read():
            dst.write(await self.exec_one(row, model, use_history))
        return dst

    def update_prompt(self, prompt: str) -> None:
        self.__prompt = prompt
