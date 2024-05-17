from __future__ import annotations

import abc
import time
import typing as tp

import torch
import transformers
import peft

from src.utils import colourful_cmd
from src.database import database_entities
from configs import local_model_settings as model_configs


class BaseModel(abc.ABC):
    def __init__(
            self,
            model_name: str,
            model_type: str,
            model_description: str,
            prompt: str,
            prompt_desc: str = "",
    ):
        self.model_name: str = model_name
        self.model_type = model_type
        self.model_description = model_description
        self.prompt = prompt
        self.prompt_desc = prompt_desc

    @property
    def database_name(self) -> str:
        return (
            self.model_name.replace('/', '_').replace('-', '_')
            + ('_' + self.prompt_desc if self.prompt_desc else '')
            + '_' + self.model_type
        )

    @abc.abstractmethod
    def get_prompt(self, data_row: database_entities.BaseEntity) -> str:
        """Generate prompt for specific task"""

    @abc.abstractmethod
    def _predict(self, prompt: str, **generation_kwargs) -> str:
        """Generate model response"""

    @abc.abstractmethod
    def _get_final_result(self, model_response: str) -> str:
        """Transform model response"""

    @abc.abstractmethod
    def clear_model(self) -> None:
        """Clear model"""

    def generate_result(
            self,
            data_row: database_entities.BaseEntity,
            **generation_kwargs
    ) -> str:
        prompt = self.get_prompt(data_row)
        model_response = self._predict(prompt, **generation_kwargs)

        return self._get_final_result(model_response)


class BaseLocalModel(BaseModel, abc.ABC):
    def __init__(
            self,
            model_name: str,
            model_type: str,
            model_description: str,
            prompt: str,
            prompt_desc: str,
            device: torch.device = model_configs.DEVICE,
            weight_type: torch.dtype = model_configs.WEIGHT_TYPE,
            lora_part_path: tp.Optional[str] = None,
    ):
        super().__init__(
            model_name=model_name,
            model_type=model_type,
            model_description=model_description,
            prompt=prompt,
            prompt_desc=prompt_desc,
        )
        self._model = None
        self._tokenizer = None
        self._generation_config = None
        self.device = device
        self.weight_type = weight_type
        self.lora_part_path = lora_part_path

    def _load_model(self) -> None:
        start = time.time()
        colourful_cmd.print_cyan(
            f'Starting to load model {self.model_name}'
        )

        self._generation_config = transformers.GenerationConfig.from_pretrained(
            self.model_name,
            max_new_tokens=model_configs.MAX_NEW_TOKENS,
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
                torch_dtype=self.weight_type if self.lora_part_path is None else None,
                device_map=self.device,
                trust_remote_code=True,
            )
        )

        if self.lora_part_path:
            self._model.config.vocab_size = model_configs.NUM_EMBEDDINGS

            tmp = self._model.model.embed_tokens.weight
            self._model.model.embed_tokens = torch.nn.Embedding(
                model_configs.NUM_EMBEDDINGS,
                model_configs.EMBEDDING_DIM
            )
            self._model.model.embed_tokens.weight.data = tmp[:model_configs.NUM_EMBEDDINGS, :]

            tmp = self._model.lm_head.weight
            self._model.lm_head = torch.nn.Linear(model_configs.EMBEDDING_DIM, model_configs.NUM_EMBEDDINGS)
            self._model.lm_head.weight.data = tmp[:model_configs.NUM_EMBEDDINGS, :]

            self._model = peft.PeftModel.from_pretrained(
                self._model,
                self.lora_part_path,
                ignore_mismatched_sizes=True,
            )

            self._model = self._model.to(self.device)

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
