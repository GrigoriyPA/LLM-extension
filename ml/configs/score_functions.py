import enum
import g4f

@enum.unique
class GPTModelName(enum.Enum):
    gpt_35_turbo = "gpt_4_turbo"
    command_r_plus = "command_r_plus"
    llama3_70b_instruct = "llama3_70b_instruct"
    llama2_70b = "llama2_70b"
    default = "default"


@enum.unique
class GPTProviderName(enum.Enum):
    FreeGpt = "FreeGpt"
    Liaobots = "Liaobots"
    You = "You"
    Feedough = "Feedough"
    Llama = "Llama"
    FlowGpt = "FlowGpt"
    Aichatos = "Aichatos"
    DeepInfra = "DeepInfra"
    PerplexityAi = "PerplexityAi"
    DuckDuckGo = "DuckDuckGo"
    Theb = "Theb"
    Bing = "Bing"



DEFAULT_FUNCTION = GPTModelName.default # for provider You it is gpt-3.5-turbo

DEFAULT_PROVIDER = GPTProviderName.You


DEFAULT_CONTEXT_LENGTH = 4096
SLEEP_TIME_SEC = 2
