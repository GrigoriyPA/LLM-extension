import enum

from models import docstring_model


@enum.unique
class DocstringModels(enum.Enum):
    microsoft_phi2 = docstring_model.DocstringModel("microsoft/phi-2", "2.7B params")
    stable_code_3b = docstring_model.DocstringModel("stabilityai/stable-code-3b", "3B params")
    # codellama_python_7b = docstring_model.DocstringModel("codellama/CodeLlama-7b-Python-hf", "CodeLLama Python 7B")
