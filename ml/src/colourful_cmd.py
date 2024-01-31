from src import constants


def _print(*args, color: str, **kwargs):
    print(color, ' '.join(map(str, args)), sep='')


def print_green(*args, **kwargs):
    _print(*args, color=constants.CmdModes.green.value, **kwargs)


def print_cyan(*args, **kwargs):
    _print(*args, color=constants.CmdModes.cyan.value, **kwargs)


def print_error(*args, **kwargs):
    _print(*args, color=constants.CmdModes.fail.value, **kwargs)