import re
import typing as tp
import g4f.client
from tqdm import tqdm
import g4f

from constants import score_functions as score_functions_constants
from models import base_model as base_model_module
from src import database_entities
from src import database_utils
import time


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
            self.current_length -= len(removed_message["content"]) if removed_message["content"] is not None else 0

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
        model_response = None
        ind = 0
        while model_response is None:
            try:
                if ind > 0:
                    self.__model = GenerativeModel()
                ind += 1
                history = self.__session_info.get_history() \
                    if use_history else [content]
                model_response = await self.__model.get_answer(history)
  
            except Exception as e:
                print(f"{self.__model.get_provider_name()}:", e)
                model_response = None
                time.sleep(score_functions_constants.SLEEP_TIME_SEC)

        self.__session_info.add_content({"role": "assistant", "content": model_response})
        return model_response

    @staticmethod
    def extract_score(answer: str) -> tp.Optional[float]:
        res = 0
        if answer is not None:
            match = re.search(r"Score: (\d+\.\d+)", answer)
            if match and match.lastgroup:
                res = float(match.lastgroup)
            else:
                match = re.findall(r"[-+]?\d*\.\d+|\d+", answer)
                if not match:
                    res = 0
                else:
                    res = float(match[-1])
        if res < 0 or res > 1:
            return 0
        return res
    
    async def get_text_score_and_output(
        self,
        function: database_entities.Function,
        use_history: bool = False
    ) -> tp.Tuple[float, str]:
        if function.docstring is None:
            return None, 0, None
        text = self.prepare_prompt(function)
        output = await self.get_model_response(
            user_input=text,
            use_history=use_history,
        )
        score = self.extract_score(output)
        return text, score, output

    async def exec_one(
            self,
            function: database_entities.Function,
            model: tp.Optional[base_model_module.BaseModel] = None,
            use_history: bool = False
    ) -> database_entities.ScorerModelDocstringResult:
        
        text, score, output = await self.get_text_score_and_output(function, use_history)
        result = database_entities.ScorerModelDocstringResult(
            **function.__dict__,
            model_name=model.model_name if model is not None else "-",
            prompt=model.get_prompt_for_docstring_generation(function) if model is not None else "-",
            scorer_prompt=text,
            docstring_score=score,
            scorer_response=output,
        )

        return result

    async def exec(
            self,
            src: database_utils.Table[database_entities.Function],
            model: tp.Optional[base_model_module.BaseModel] = None,
            dst: tp.Optional[
                database_utils.Table[database_entities.ScorerModelDocstringResult]
            ] = None,
            use_history: bool = False,
            debug: bool = False, 
            start_index: int = 0
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
                table_name=f'scorer_{(model.model_name if model is not None else "default")}_results'
            )
        index = 0
        for row in src.read() if not debug else tqdm(src.read()):
            if index >= start_index:
                dst.write(await self.exec_one(row, model, use_history))
            index += 1
        return dst

    def update_prompt(self, prompt: str) -> None:
        self.__prompt = prompt
