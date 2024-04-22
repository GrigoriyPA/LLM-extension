import enum

from models import local_hf_model


@enum.unique
class LanguageModel(enum.Enum):
    microsoft_phi2 = local_hf_model.LocalHFModel("microsoft/phi-2", "2.7B params")
    stable_code_3b = local_hf_model.LocalHFModel("stabilityai/stable-code-3b", "3B params")
    codellama_python_7b = local_hf_model.LocalHFModel("codellama/CodeLlama-7b-Python-hf", "CodeLLama Python 7B")
