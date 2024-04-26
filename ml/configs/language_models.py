import enum

from models import docstring_model
from models import tests_generation_model


@enum.unique
class DocstringModels(enum.Enum):
    llama_model = docstring_model.DocstringApiModel("llama3_70b_instruct", model_description="70B params")
    microsoft_phi2 = docstring_model.DocstringLocalModel("microsoft/phi-2", "2.7B params")
    microsoft_phi3 = docstring_model.DocstringLocalModel("microsoft/Phi-3-mini-128k-instruct", "3.6B params")
    stable_code_3b = docstring_model.DocstringLocalModel("stabilityai/stable-code-3b", "3B params")
    codellama_instruct_8b = docstring_model.DocstringLocalModel("meta-llama/Meta-Llama-3-8B-Instruct", "Lama 3 instruct")


@enum.unique
class TestGenerationModels(enum.Enum):
    llama_model = tests_generation_model.TestGenerationApiModel("llama3_70b_instruct", model_description= "70B params")
    microsoft_phi3 = tests_generation_model.TestGenerationLocalModel("microsoft/Phi-3-mini-128k-instruct", "3.6B params")
    microsoft_phi2 = tests_generation_model.TestGenerationLocalModel("microsoft/phi-2", "2.7B params")
    stable_code_3b = tests_generation_model.TestGenerationLocalModel("stabilityai/stable-code-3b", "3B params")
    # codellama_instruct_8b = tests_generation_model.TestGenerationLocalModel("meta-llama/Meta-Llama-3-8B-Instruct", "Lama 3 instruct")
