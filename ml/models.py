import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
import torch

import time
from typing import Optional
from textwrap import dedent
import pandas as pd
import datetime

from text_data.prompts import DOCSTRING_PROMPT


class IdeLLM:
    def __init__(self, checkpoint: str):
        self._checkpoint: str = checkpoint
        self._tokenizer = AutoTokenizer.from_pretrained(checkpoint)

        start = time.time()
        print(f'Starting to load model {checkpoint}')
        self._model: transformers.PreTrainedModel = AutoModelForCausalLM.from_pretrained(checkpoint,
                                                                             low_cpu_mem_usage=True,
                                                                             torch_dtype="auto",
                                                                             device_map="auto")
        finish = time.time()
        print(f'Finished loading model {checkpoint}, it took {round(finish - start, 1)} seconds')

        self._generation_config = GenerationConfig.from_pretrained(
            self._checkpoint,
            max_new_tokens=200,
        )

        self._docstring_prompt = DOCSTRING_PROMPT
        # TODO there must be some fewshot examples after that prompt

    def generate_docstring(self,
                           function: str,
                           context: Optional[str] = "",
                           **generation_params) -> (str, str):
        """
        Returns docstring for the function by the given description

        You have to pass declaration and optional definition with context of your function.
        Prompt will be built by using all that information, so be careful when passing it

        :param str function: full code of your function or class (e.g. def sum(a, b, c): return a + b + c)
        :param str context: context of usages of your func
        :param generation_params: generation params, which will be directly passed to the model generate() method

        :return: docstring for your function or class
        """

        context = f"\nHere you can see examples of usages of such function:\n{context}" if context else ""
        full_prompt = dedent(f'''
        {self._docstring_prompt}
        {function}{context}
        Docstring for that function:''')

        model_inputs = self._tokenizer(full_prompt, return_tensors='pt')
        generated_ids = self._model.generate(**model_inputs, generation_config=self._generation_config)
        generated_docstring = self._tokenizer.batch_decode(
            generated_ids[:, model_inputs["input_ids"].shape[1]:],
            skip_special_tokens=True
        )[0].strip("\n").strip("")

        return full_prompt, generated_docstring


def launch_models(model_names, dst_path, query):
    try:
        df = pd.read_csv(dst_path, sep=';')
    except FileNotFoundError:
        open(dst_path)
        df = pd.read_csv(dst_path, sep=';')

    for model_name in model_names:
        model = IdeLLM(model_name)
        prompt, model_answer = model.generate_docstring(query)
        df = df._append({
            'model': model_name,
            'query': query,
            'prompt': prompt,
            'answer': model_answer,
            'gpt_score': 1,
            'time': str(datetime.datetime.now()),
        }, ignore_index=True)
        print(prompt, model_answer)

    df.to_csv(dst_path, sep=";")


model_names = ["codellama/CodeLlama-7b-hf", "codellama/CodeLlama-7b-Python-hf", "codellama/CodeLlama-7b-Instruct-hf"]
dst_path = "text_data/bench_results.csv"
query = """def check(dic, need):
                    dicSet = set(dic.keys())
                    if dicSet != need:
                        missing = need.difference(dicSet)
                        return False, missing.pop()
                    return True, None"""


launch_models(model_names, dst_path, query)
