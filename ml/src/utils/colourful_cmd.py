import enum


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


def _print(*args, color: str, **kwargs) -> None:
    print(
        color,
        ' '.join(map(str, args)) + CmdModes.endc.value,
        sep='',
        **kwargs
    )


def print_green(*args, **kwargs) -> None:
    _print(*args, color=CmdModes.green.value, **kwargs)


def print_cyan(*args, **kwargs) -> None:
    _print(*args, color=CmdModes.cyan.value, **kwargs)


def print_red(*args, **kwargs) -> None:
    _print(*args, color=CmdModes.fail.value, **kwargs)
