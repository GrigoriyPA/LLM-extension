import enum


@enum.unique
class GPTModelName(enum.Enum):
    default = "gpt_4"


@enum.unique
class GPTProviderName(enum.Enum):
    default = "FreeGpt"
