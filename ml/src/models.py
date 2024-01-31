import datetime
import json
import time
import typing as tp
from textwrap import dedent

import transformers
from src.colourful_cmd import print_cyan, print_green, print_error
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig

from text_data.prompts import DOCSTRING_PROMPT


class IdeLLM:
    def __init__(self, checkpoint_path: str):
        self._checkpoint: str = checkpoint_path
        self._tokenizer = AutoTokenizer.from_pretrained(checkpoint_path)

        start = time.time()
        print_cyan(f'Starting to load model {checkpoint_path}')
        self._model: transformers.PreTrainedModel = (
            AutoModelForCausalLM.from_pretrained(
                pretrained_model_name_or_path=checkpoint_path,
                low_cpu_mem_usage=True,
                torch_dtype="auto",
                device_map="auto"
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
        # TODO there must be some fewshot examples after that prompt

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


def launch_models(model_names, dst_path, query):
    with open(dst_path) as f:
        text = f.read()
        if not text:
            text = '[]'
        data = json.loads(text)

    total_time = time.time()
    print_cyan("Starting testing models")

    for model_name in model_names:
        try:
            model = IdeLLM(model_name)

            cur_time = time.time()
            print_cyan(f"Testing model {model_name} now")
            prompt, model_answer = model.generate_docstring(query)
            data.append({
                'model': model_name,
                'query': query,
                'prompt': prompt,
                'answer': model_answer,
                'score': 1,
                'time': str(datetime.datetime.now()),
            })
            print_green(
                f"Finished testing model {model_name},"
                f" it took {round(time.time() - cur_time, 1)} seconds"
            )
        except BaseException:
            print_error(
                f"There was a mistake while processing model {model_name}"
            )

    with open(dst_path, 'w') as f:
        json.dump(data, f, indent=4)

    print_green(
        f"Finished testing models,"
        f" it took {round(time.time() - total_time, 1)} seconds"
    )


def print_results(dst_path):
    with open(dst_path) as f:
        data = json.load(f)

    for el in data:
        print_green(el['model'], el['answer'], sep='\n')
