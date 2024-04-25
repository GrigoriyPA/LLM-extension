from __future__ import annotations

import abc
import time

import torch
import transformers


from src import colourful_cmd
from src import database_entities
from configs import local_model_settings as model_configs


class BaseModel(abc.ABC):
    def __init__(
            self,
            model_name: str,
            model_description: str,
            device: torch.device = model_configs.DEVICE,
            weight_type: torch.dtype = model_configs.WEIGHT_TYPE,
    ):
        self.model_name: str = model_name
        self.model_description = model_description
        self._model = None
        self._tokenizer = None
        self._generation_config = transformers.GenerationConfig.from_pretrained(
            self.model_name,
            max_new_tokens=256
        )
        self.device = device
        self.weight_type = weight_type

    @property
    def database_name(self) -> str:
        return self.model_name.replace('/', '_').replace('-', '_')

    def _load_model(self) -> None:
        start = time.time()
        colourful_cmd.print_cyan(
            f'Starting to load model {self.model_name}'
        )
        self._tokenizer = transformers.AutoTokenizer.from_pretrained(
            pretrained_model_name_or_path=self.model_name,
            device_map=self.device,
            trust_remote_code=True,
        )
        self._model: transformers.PreTrainedModel = (
            transformers.AutoModelForCausalLM.from_pretrained(
                pretrained_model_name_or_path=self.model_name,
                low_cpu_mem_usage=True,
                torch_dtype=self.weight_type,
                device_map=self.device,
                trust_remote_code=True,
            )
        )
        finish = time.time()
        colourful_cmd.print_green(
            f'Finished loading model {self.model_name},'
            f' it took {round(finish - start, 1)} seconds'
        )

    def _check_model(self):
        if self._model is None:
            self._load_model()

    def clear_model(self) -> None:
        del self._model
        del self._tokenizer
        if self.device == torch.device('cuda:0'):
            torch.cuda.empty_cache()

    @abc.abstractmethod
    def get_prompt(self, data_row: database_entities.BaseEntity) -> str:
        """Generate prompt for specific task"""

    def _predict(self, prompt: str, **generation_kwargs) -> str:
        self._check_model()
        model_inputs = self._tokenizer(prompt, return_tensors='pt')
        model_inputs = model_inputs.to(self.device)
        generated_ids = self._model.generate(
            **model_inputs,
            generation_config=self._generation_config,
            **generation_kwargs,
        )
        generated_text = self._tokenizer.batch_decode(
            generated_ids[:, model_inputs["input_ids"].shape[1]:],
            skip_special_tokens=True)[0].strip("\n").strip("")
        return generated_text

    @abc.abstractmethod
    def _get_final_result(self, model_response: str) -> str:
        """Transform model response"""

    def generate_result(
            self,
            data_row: database_entities.BaseEntity,
            **generation_kwargs
    ) -> str:
        prompt = self.get_prompt(data_row)
        model_response = self._predict(prompt, **generation_kwargs)

        return self._get_final_result(model_response)
