from os.path import expanduser
from textwrap import dedent

import replicate

from configs.features_config import ExtensionFeature
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


class CodeLLama70B(BaseModel):
    def __init__(self):
        super().__init__("CodeLLama 70B", "CodeLLama 70B api using replicate lib")

        self._docstring_prompt = DOCSTRING_PROMPT
        self.client = replicate.Client(
            api_token=REPLICATE_TOKEN,
        )
        self.api_model_path = \
            "meta/codellama-70b-instruct:a279116fe47a0f65701a8817188601e2fe8f4b9e04a518789655ea7b995851bf"

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
        return self.predict(self.get_prompt_for_docstring_generation(function))


model = CodeLLama70B()
print(model.generate_docstring(Function("sum", "def sum(a, b): return a + b", "", "")))
