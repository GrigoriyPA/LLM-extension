import enum

from models import docstring_model
from models import docstring_llama_model


@enum.unique
class DocstringModels(enum.Enum):
    docstring_llama_model = docstring_llama_model.DocstringLLamaModel("llama3_70b_instruct", "70B params")
    microsoft_phi2 = docstring_model.DocstringModel("microsoft/phi-2", "2.7B params")
    microsoft_phi3 = docstring_model.DocstringModel("microsoft/Phi-3-mini-128k-instruct", "3.6B params")
    stable_code_3b = docstring_model.DocstringModel("stabilityai/stable-code-3b", "3B params")
    codellama_instruct_8b = docstring_model.DocstringModel("meta-llama/Meta-Llama-3-8B-Instruct", "Lama 3 instruct")

