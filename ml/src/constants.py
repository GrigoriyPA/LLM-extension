import enum


@enum.unique
class LanguageModelName(enum.Enum):
    code_lama_7b = "codellama/CodeLlama-7b-hf"
    code_lama_7b_python = "codellama/CodeLlama-7b-Python-hf"
    code_lama_7b_instruct = "codellama/CodeLlama-7b-Instruct-hf",
    code_lama_13b_python = "codellama/CodeLlama-13b-Python-hf"
    code_lama_13b_instruct = "codellama/CodeLlama-13b-Instruct-hf"


@enum.unique
class CmdModes(enum.Enum):
    header = '\033[95m'
    blue = '\033[94m'
    cyan = '\033[96m'
    green = '\033[92m'
    warn = '\033[93m'
    fail = '\033[91m'
    endc = '\033[0m'
    bold = '\033[1m'
    underline = '\033[4m'
