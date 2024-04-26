import enum

from models import docstring_model
from models import docstring_llama_model


@enum.unique
class DocstringModels(enum.Enum):
<<<<<<< HEAD
    docstring_llama_model = docstring_llama_model.DocstringLLamaModel("llama3_70b_instruct", "70B params")
    microsoft_phi2 = docstring_model.DocstringModel("microsoft/phi-2", "2.7B params")
    stable_code_3b = docstring_model.DocstringModel("stabilityai/stable-code-3b", "3B params")
    codellama_python_7b = docstring_model.DocstringModel("codellama/CodeLlama-7b-Python-hf", "CodeLLama Python 7B")
    docstring_llama_model = docstring_llama_model.DocstringLLamaModel()
=======
    microsoft_phi2 = docstring_model.DocstringModel("microsoft/phi-2 with default prompt", "2.7B params")
    stable_code_3b = docstring_model.DocstringModel("stabilityai/stable-code-3b with default prompt", "3B params")
    codellama_python_7b = docstring_model.DocstringModel("codellama/CodeLlama-7b-Python-hf with default prompt",
                                                         "CodeLLama Python 7B")
    docstring_llama_model = docstring_llama_model.DocstringLLamaModel("API LLama with default prompt")
>>>>>>> 2e23d6d (added new docstring prompts)
