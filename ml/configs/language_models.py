import enum

from models import docstring_model
from models import tests_generation_model


@enum.unique
class DocstringModels(enum.Enum):
    docstring_llama_model = docstring_model.DocstringApiModel("llama3_70b_instruct",
                                                              model_description="70B params")
    microsoft_phi2 = docstring_model.DocstringLocalModel("microsoft/phi-2", "2.7B params")
    microsoft_phi3 = docstring_model.DocstringLocalModel("microsoft/Phi-3-mini-128k-instruct", "3.6B params")
    stable_code_3b = docstring_model.DocstringLocalModel("stabilityai/stable-code-3b", "3B params")
    codellama_python_7b = docstring_model.DocstringLocalModel("codellama/CodeLlama-7b-Python-hf",
                                                              "CodeLLama Python 7B")
    codellama_instruct_7b = docstring_model.DocstringLocalModel("codellama/CodeLlama-7b-Instruct-hf",
                                                                "CodeLLama Instruct 7B")


@enum.unique
class TestGenerationModels(enum.Enum):
    llama_model = tests_generation_model.TestGenerationApiModel("llama3_70b_instruct", model_description="70B params")
    microsoft_phi3 = tests_generation_model.TestGenerationLocalModel("microsoft/Phi-3-mini-128k-instruct",
                                                                     "3.6B params")
    microsoft_phi2 = tests_generation_model.TestGenerationLocalModel("microsoft/phi-2", "2.7B params")
    stable_code_3b = tests_generation_model.TestGenerationLocalModel("stabilityai/stable-code-3b", "3B params")
