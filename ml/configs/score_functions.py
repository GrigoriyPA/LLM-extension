import enum


@enum.unique
class GPTModelName(enum.Enum):
    gpt_35_turbo = "gpt_35_turbo"
    command_r_plus = "command_r_plus"
    llama3_70b_instruct = "llama3_70b_instruct"


@enum.unique
class GPTProviderName(enum.Enum):
    FreeGpt = "FreeGpt"
    Liaobots = "Liaobots"
    You = "You"
    Feedough = "Feedough"
    Llama = "Llama"


DEFAULT_FUNCTION = GPTModelName.gpt_35_turbo
DEFAULT_PROVIDER = GPTProviderName.FreeGpt


DEFAULT_CONTEXT_LENGTH = 4096
SLEEP_TIME_SEC = 1
