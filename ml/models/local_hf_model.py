import time
import re
from textwrap import dedent

import torch
import transformers

from configs.device_type import DEVICE
from configs import prompts
from models import base_model as base_model_module
from src import colourful_cmd
from src import database_entities


class LocalHFModel(base_model_module.BaseModel):
    def __init__(self,
                 model_name: str,
                 model_description: str):
        super().__init__(model_name, model_description)

        self._checkpoint: str = model_name
        self._tokenizer = transformers.AutoTokenizer.from_pretrained(
            self._checkpoint,
            device_map=DEVICE,
            trust_remote_code=True,
        )
        self._generation_config = transformers.GenerationConfig.from_pretrained(
            self._checkpoint,
            max_new_tokens=200,
        )
        self._docstring_prompt = prompts.DOCSTRING_PROMPT
        self._model = None

    def _load_model(self) -> None:
        start = time.time()
        colourful_cmd.print_cyan(
            f'Starting to load model {self._checkpoint}'
        )
        self._model: transformers.PreTrainedModel = (
            transformers.AutoModelForCausalLM.from_pretrained(
                pretrained_model_name_or_path=self._checkpoint,
                low_cpu_mem_usage=True,
                torch_dtype=torch.float32,
                device_map=DEVICE,
                trust_remote_code=True,
            )
        )
        finish = time.time()
        colourful_cmd.print_green(
            f'Finished loading model {self._checkpoint},'
            f' it took {round(finish - start, 1)} seconds'
        )

    def _check_model(self):
        if self._model is None:
            self._load_model()

    def predict(self, prompt: str, **generation_kwargs) -> str:
        self._check_model()
        model_inputs = self._tokenizer(prompt, return_tensors='pt')
        model_inputs.to(DEVICE)
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
                                            function: database_entities.Function,
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
                           function: database_entities.Function,
                           **generation_kwargs) -> str:
        prompt = self.get_prompt_for_docstring_generation(function)
        result = self.predict(prompt, **generation_kwargs)
        regexp_result = re.search('"""(.*?)"""', result, re.DOTALL)
        docstring = regexp_result.group(1) if regexp_result else result
        return docstring
