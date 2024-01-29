class CmdColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def _print(color, text):
    print(color + text + CmdColors.ENDC)


def print_green(text):
    _print(CmdColors.OKGREEN, text)


def print_cyan(text):
    _print(CmdColors.OKCYAN, text)


def print_red(text):
    _print(CmdColors.FAIL, text)
