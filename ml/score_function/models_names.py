import enum


@enum.unique
class GPTModelName(enum.Enum):
    default = "gpt_35_turbo"


@enum.unique
class GPTProviderName(enum.Enum):
    default = "FlowGpt"
