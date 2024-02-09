import enum


@enum.unique
class LanguageModelName(enum.Enum):
    microsoft_phi2 = "microsoft/phi-2"
    stable_code_3b = "stabilityai/stable-code-3b"
