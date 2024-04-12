import re
from os.path import expanduser
from textwrap import dedent

import replicate

from configs.prompts import DOCSTRING_PROMPT
from models.base_model import BaseModel
from src.colourful_cmd import print_cyan
from src.entities import Function

# register and get token here https://replicate.com/

REPLICATE_TOKEN_PATH = expanduser('~/.llm_hse/replicate_token')

try:
    with open(REPLICATE_TOKEN_PATH, 'r') as file:
        REPLICATE_TOKEN = file.read().strip()
except FileNotFoundError:
    print_cyan(f"You must specify you github api token in {REPLICATE_TOKEN_PATH}")
    raise


class ReplicateModel(BaseModel):
    def __init__(self, model_name: str, model_description: str, api_model_path: str):
        super().__init__(model_name, model_description)

        self._docstring_prompt = DOCSTRING_PROMPT
        self.client = replicate.Client(
            api_token=REPLICATE_TOKEN,
        )
        self.api_model_path = api_model_path

    def predict(self, prompt: str, *args, **kwargs) -> str:
        output = self.client.run(
            self.api_model_path,
            input={
                "prompt": prompt,
            }
        )
        return "".join(output)

    def get_prompt_for_docstring_generation(self, function: Function) -> str:
        context = (
            f"\nHere you can see examples of"
            f" usages of such function:\n{function.context}"
            if function.context else ""
        )
        full_prompt = dedent(f'''
        {self._docstring_prompt}
        {function.code}{context}
        Docstring for that function:''')

        return full_prompt

    def generate_docstring(self, function: Function) -> str:
        result = self.predict(self.get_prompt_for_docstring_generation(function))
        regexp_result = re.search('"""(.*?)"""', result, re.DOTALL)
        docstring = regexp_result.group(1) if regexp_result else result
        return docstring
