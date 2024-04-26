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
        self.__session_info = SessionInfo()
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
                    self.__model = getattr(
                        g4f.models,
                        score_functions_constants.DEFAULT_FUNCTION.value
                    )
                ind += 1
                history = self.__session_info.get_history() \
                    if use_history else [content]
                model_response = await self.get_answer(history)
  
            except Exception as e:
                print(f"{self.__model.get_provider_name()}:", e)
                model_response = None
                time.sleep(score_functions_constants.SLEEP_TIME_SEC)

        self.__session_info.add_content({"role": "assistant", "content": model_response})
        return model_response


class ScoreFunction:
    def __init__(
            self,
            prompt: str,
            scored_entity_type: tp.Type[database_entities.SCORED_ENTITY_TYPE],
            model: GenerativeModel = GenerativeModel(),
    ):
        self.__model: GenerativeModel = model
        self.prompt: str = prompt
        self.scored_entity_type = scored_entity_type

    def prepare_prompt(self, entity: tp.Optional[database_entities.ENTITY_TYPE]) -> tp.Optional[str]:
        return self.prompt.format(**entity.__dict__)

    async def get_model_response(
            self,
            user_input: str,
            use_history: bool,
    ) -> str:
        return await self.__model.get_model_response(user_input, use_history)

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

    @staticmethod
    def check_all_fields(entity: database_entities.ENTITY_TYPE):
        if entity == database_entities.Function:
            return bool(entity.docstring)
        return True

    async def get_text_score_and_output(
            self,
            entity: database_entities.ENTITY_TYPE,
            use_history: bool = False
    ) -> tp.Tuple[tp.Optional[str], tp.Optional[float], tp.Optional[str]]:
        if not self.check_all_fields(entity):
            return None, 0, None
        text = self.prepare_prompt(entity)
        output = await self.get_model_response(
            user_input=text,
            use_history=use_history,
        )
        score = self.extract_score(output)
        return text, score, output

    async def exec_one(
            self,
            entity: database_entities.ENTITY_TYPE,
            model: tp.Optional[base_model_module.BaseModel] = None,
            use_history: bool = False
    ) -> database_entities.SCORED_ENTITY_TYPE:
        text, score, output = await self.get_text_score_and_output(entity, use_history)
        result = self.scored_entity_type(
            **entity.__dict__,
            model_name=model.model_name if model is not None else "-",
            prompt=model.get_prompt(entity) if model is not None else "-",
            scorer_prompt=text,
            docstring_score=score,
            scorer_response=output,
        )
        return result

    async def exec(
            self,
            src: database_utils.Table[database_entities.ENTITY_TYPE],
            model: tp.Optional[base_model_module.BaseModel] = None,
            dst: tp.Optional[
                database_utils.Table[database_entities.SCORED_ENTITY_TYPE]
            ] = None,
            use_history: bool = False,
            debug: bool = True,
            start_index: int = 0
    ) -> database_utils.Table[database_entities.ScorerModelDocstringResult]:
        """
        Scores every function in src dataset and writes result to dst dataset
        :param src: Dataset of Function elements
        :param model: Model which was used for predictions
        :param dst: Dataset of ModelDocstringResult elements,
        if not passed then tmp table will be created and returned
        :param use_history: use history
        :param debug: debug mode
        :param start_index: first row to be scored
        """
        if not dst:
            dst = database_utils.create_new_table(
                row_type=self.scored_entity_type,
                table_name=f'scorer_{(model.database_name if model is not None else "default")}_results'
            )
        index = 0
        for row in src.read() if not debug else tqdm(src.read()):
            if index >= start_index:
                dst.write(await self.exec_one(row, model, use_history))
            index += 1
        return dst

    def update_prompt(self, prompt: str) -> None:
        self.prompt = prompt
