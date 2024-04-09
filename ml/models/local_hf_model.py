import time
from textwrap import dedent

from src.colourful_cmd import print_cyan, print_green

from src.entities import Function
from configs.prompts import DOCSTRING_PROMPT
from models.base_model import BaseModel
import torch
import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig


class LocalHFModel(BaseModel):
    def __init__(self,
                 model_name: str,
                 model_description: str):
        super().__init__(model_name, model_description)

        self._checkpoint: str = model_name
        self._tokenizer = AutoTokenizer.from_pretrained(
            self._checkpoint,
            device_map="auto",
            trust_remote_code=True,
        )
        self._generation_config = GenerationConfig.from_pretrained(
            self._checkpoint,
            max_new_tokens=200,
        )
        self._docstring_prompt = DOCSTRING_PROMPT
        self._model = None
        self._load_model()

    def _load_model(self) -> None:
        start = time.time()
        print_cyan(f'Starting to load model {self._checkpoint}')
        self._model: transformers.PreTrainedModel = (
            AutoModelForCausalLM.from_pretrained(
                pretrained_model_name_or_path=self._checkpoint,
                low_cpu_mem_usage=True,
                torch_dtype=torch.float32,
                device_map="auto",
                trust_remote_code=True,
            )
        )
        finish = time.time()
        print_green(
            f'Finished loading model {self._checkpoint},'
            f' it took {round(finish - start, 1)} seconds'
        )

    def predict(self, prompt: str, **generation_kwargs) -> str:
        model_inputs = self._tokenizer(prompt, return_tensors='pt')
        generated_ids = self._model.generate(
            **model_inputs,
            generation_config=self._generation_config,
            **generation_kwargs,
        )
        generated_text = self._tokenizer.batch_decode(
            generated_ids[:, model_inputs["input_ids"].shape[1]:],
            skip_special_tokens=True)[0].strip("\n").strip("")
        return generated_text

    def get_prompt_for_docstring_generation(self,
                                            function: Function,
                                            *args,
                                            **kwargs) -> str:
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

    def generate_docstring(self,
                           function: Function,
                           **generation_kwargs) -> str:
        prompt = self.get_prompt_for_docstring_generation(function)
        generated_docstring = self.predict(prompt, **generation_kwargs)
        return generated_docstring
