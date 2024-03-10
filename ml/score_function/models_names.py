import enum


@enum.unique
class GPTModelName(enum.Enum):
    gpt_4 = "gpt_4"


@enum.unique
class GPTProviderName(enum.Enum):
    you = "You"
