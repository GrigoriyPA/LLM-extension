import enum

from models.api_models import ReplicateModel
from models.local_hf_model import LocalHFModel


@enum.unique
class LanguageModel(enum.Enum):
    microsoft_phi2 = LocalHFModel("microsoft/phi-2", "2.7B params")
    stable_code_3b = LocalHFModel("stabilityai/stable-code-3b", "3B params")
    codellama_python_70b = ReplicateModel("CodeLLama Python 70B",
                                          "CodeLLama Python 70B from replicate",
                                          "meta/codellama-70b-python:"
                                          "338f2fc1036f847626d0905c1f4fbe6d6d287a476c655788b3f1f27b1a78dab2")
    codellama_python_7b = ReplicateModel("CodeLLama Python 7B",
                                         "CodeLLama Python 7B from replicate",
                                         "nateraw/codellama-7b-python:"
                                         "cba55291fed53180af7f5ea0f3681b7b763eb2a1783fc4ca517df32206fbfae6")
    wizard_coder_34b = ReplicateModel("WizardCoder 34B",
                                      "WizardCoder 34B from replicate",
                                      "nateraw/wizardcoder-python-34b-v1.0:"
                                      "7cccdb1f912482eb5b2f5671d23e6a6313ab0e101aa15a915ec777ed8521a85b")