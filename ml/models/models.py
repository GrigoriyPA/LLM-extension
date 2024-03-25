import time
import torch
import typing as tp
from textwrap import dedent

import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig

from utils.colourful_cmd import print_cyan, print_green, print_red
from datasets.prompts import DOCSTRING_PROMPT


class IdeLLM:
    def __init__(self, checkpoint_path: str):
        self._checkpoint: str = checkpoint_path
        self._tokenizer = AutoTokenizer.from_pretrained(
            checkpoint_path,
            device_map="auto",
            trust_remote_code=True,
        )

        start = time.time()
        print_cyan(f'Starting to load model {checkpoint_path}')
        self._model: transformers.PreTrainedModel = (
            AutoModelForCausalLM.from_pretrained(
                pretrained_model_name_or_path=checkpoint_path,
                low_cpu_mem_usage=True,
                torch_dtype=torch.float32,
                device_map="auto",
                trust_remote_code=True,
            )
        )
        finish = time.time()
        print_green(
            f'Finished loading model {checkpoint_path},'
            f' it took {round(finish - start, 1)} seconds'
        )

        self._generation_config = GenerationConfig.from_pretrained(
            self._checkpoint,
            max_new_tokens=200,
        )

        self._docstring_prompt = DOCSTRING_PROMPT

    def generate_docstring(self,
                           function: str,
                           context: tp.Optional[str] = "",
                           **generation_params) -> (str, str):
        """
        Returns docstring for the function by the given description

        You have to pass declaration and optional definition
        with context of your function.
        Prompt will be built by using all that information,
        so be careful when passing it

        :param str function: full code of your function or class
        (e.g. def sum(a, b, c): return a + b + c)
        :param str context: context of usages of your func
        :param generation_params: generation params,
        which will be directly passed to the model generate() method

        :return: docstring for your function or class
        """

        context = (
            f"\nHere you can see examples of"
            f" usages of such function:\n{context}"
            if context else ""
        )
        full_prompt = dedent(f'''
        {self._docstring_prompt}
        {function}{context}
        Docstring for that function:''')

        model_inputs = self._tokenizer(full_prompt, return_tensors='pt')
        generated_ids = self._model.generate(
            **model_inputs,
            generation_config=self._generation_config,
            **generation_params
        )

        generated_docstring = self._tokenizer.batch_decode(
            generated_ids[:, model_inputs["input_ids"].shape[1]:],
            skip_special_tokens=True)[0].strip("\n").strip("")

        return full_prompt, generated_docstring
