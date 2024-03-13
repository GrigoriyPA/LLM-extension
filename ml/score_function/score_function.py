import g4f
import pandas as pd
import typing as tp
import re


class SessionInfo:
    def __init__(self, max_length: int = 4096):
        self.history: tp.List[tp.Dict[str, str]] =  []
        self.max_length: int = max_length
        self.current_length: int = 0
  
    def trim_history(self) -> None:
        while self.history and self.current_length > self.max_length:
            removed_message = self.history.pop(0)
            self.current_length -= len(removed_message["content"])
    
    def add_content(self, action: tp.Dict[str, str]):
        self.history.append(action)
        self.current_length += len(action["content"])
        self.trim_history()

    def get_history(self) -> tp.List[tp.Dict[str, str]]:
        return self.history


class GenerativeModel():
    def __init__(
            self, 
            model: tp.Union[g4f.models.Model, str], 
            provider: tp.Union[g4f.providers.types.ProviderType, str, None] = None
    ):
        self.__chat_completion = g4f.ChatCompletion
        self.__model = model
        self.__provider = provider
    
    async def get_answer(
            self, prompt: str, history: tp.List[tp.Dict[str, str]]
    ) -> str:
        return await self.__chat_completion.create_async(
            model=self.__model,
            messages=history,
            provider=self.__provider
        )


class ScoreFunction:
    def __init__(
            self,
            prompt: str,
            model: GenerativeModel,
    ):
        self.__session_info: SessionInfo = SessionInfo()
        self.__model: GenerativeModel = model
        self.__prompt: str = prompt

    def prepare_prompt(
            self,
            defin: str, 
            func_body: str
    ) -> str:
        return self.__prompt.format(defin=defin, func_body=func_body)
    
    async def get_model_response(
            self,
            user_input: str, 
            use_history: bool, 
    ) -> str:
        self.__session_info.add_content({"role": "user", "content": user_input})
        try:
            history = self.__session_info.get_history() \
                    if use_history else [{"role": "user", "content": user_input}]
            model_response = await self.__model.get_answer(user_input, history)

        except Exception as e:
            print(f"{self.__model.provider.__name__}:", e)
            model_response = None

        self.__session_info.add_content({"role": "assistant", "content": model_response})
        return model_response

    def extract_score(self, answer: str) -> float:
        numbers = re.findall(r"[-+]?\d*\.\d+|\d+", answer)
        if not numbers:
            return None
        return float(numbers[-1])

    async def exec(self, data: pd.DataFrame, use_history: bool = False) -> pd.DataFrame:
        df = data.copy()
        df['answer'] = None
        for i, row in df.iterrows():
            text = self.prepare_prompt(row['defin'], row['func_body'])
            output = await self.get_model_response(
                user_input=text,
                use_history=use_history, 
            )
            df.at[i, 'answer'] = output
            df.at[i, 'score'] = self.extract_score(output)
        return df

    def update_prompt(self, prompt: str):
        self.__prompt = prompt
