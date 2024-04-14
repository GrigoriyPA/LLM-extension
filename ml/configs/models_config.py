import enum

from models.local_hf_model import LocalHFModel


@enum.unique
class LanguageModel(enum.Enum):
    microsoft_phi2 = LocalHFModel("microsoft/phi-2", "2.7B params")
    stable_code_3b = LocalHFModel("stabilityai/stable-code-3b", "3B params")
    codellama_python_7b = LocalHFModel("codellama/CodeLlama-7b-Python-hf", "CodeLLama Python 7B")
