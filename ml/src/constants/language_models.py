import enum
import transformers

from src.models import docstring_models
from src.models import tests_generation_models
from src.models import autocomplete_models

from src.models import semantic_sense_models
from configs import prompts
from configs import local_model_settings as model_configs


@enum.unique
class DocstringModels(enum.Enum):
    docstring_llama_model = docstring_models.DocstringApiModel(
        model_name="llama3_70b_instruct",
        model_description="70B params"
    )
    microsoft_phi2 = docstring_models.DocstringLocalModel(
        model_name="microsoft/phi-2",
        model_description="2.7B params"
    )
    microsoft_phi3 = docstring_models.DocstringLocalModel(
        model_name="microsoft/Phi-3-mini-128k-instruct",
        model_description="3.6B params"
    )
    finetuned_microsoft_phi3 = docstring_models.DocstringLocalModel(
        model_name="microsoft/Phi-3-mini-128k-instruct",
        model_description="3.6B params",
        lora_part_path="finetuned_models/finetune-phi3-docstring",
        prompt=prompts.FINETUNE_DOCSTRING_PROMPT,
    )
    stable_code_3b = docstring_models.DocstringLocalModel(
        model_name="stabilityai/stable-code-3b",
        model_description="3B params"
    )
    codellama_python_7b = docstring_models.DocstringLocalModel(
        model_name="codellama/CodeLlama-7b-Python-hf",
        model_description="CodeLLama Python 7B"
    )
    codellama_instruct_7b = docstring_models.DocstringLocalModel(
        model_name="codellama/CodeLlama-7b-Instruct-hf",
        model_description="CodeLLama Instruct 7B"
    )


@enum.unique
class TestGenerationModels(enum.Enum):
    llama_model = tests_generation_models.TestGenerationApiModel(
        model_name="llama3_70b_instruct", model_description="70B params")
    microsoft_phi3 = tests_generation_models.TestGenerationLocalModel(
        model_name="microsoft/Phi-3-mini-128k-instruct",
        model_description="3.6B params"
    )
    microsoft_phi2 = tests_generation_models.TestGenerationLocalModel(
        model_name="microsoft/phi-2",
        model_description="2.7B params"
    )
    finetuned_microsoft_phi3 = tests_generation_models.TestGenerationLocalModel(
        model_name="microsoft/Phi-3-mini-128k-instruct",
        model_description="3.6B params",
        lora_part_path="finetuned_models/finetune-phi3-unit-test",
        prompt=prompts.FINETUNE_TEST_GENERATION_PROMPT,
    )
    stable_code_3b = tests_generation_models.TestGenerationLocalModel(
        model_name="stabilityai/stable-code-3b",
        model_description="3B params"
    )


class AutoCompleteModels(enum.Enum):
    microsoft_phi3 = autocomplete_models.AutoCompleteLocalModel(
        model_name="microsoft/Phi-3-mini-128k-instruct",
        model_description="3.6B params",
        prompt=prompts.EMPTY_AUTOCOMPLETE_PROMPT,
        generation_config=transformers.GenerationConfig.from_pretrained(
            "microsoft/Phi-3-mini-128k-instruct",
            max_new_tokens=model_configs.AUTOCOMPLETE_MAX_NEW_TOKENS,
        )
    )


class SemanticSenseModels(enum.Enum):
    microsoft_phi3 = semantic_sense_models.SemanticSenseLocalModel(
        model_name="microsoft/Phi-3-mini-128k-instruct",
        model_description="3.6B params"
    )
