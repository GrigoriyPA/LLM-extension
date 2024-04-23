import enum


@enum.unique
class GPTModelName(enum.Enum):
    gpt_35_turbo = "gpt_35_turbo"


@enum.unique
class GPTProviderName(enum.Enum):
    FreeGpt = "FreeGpt"
    Liaobots = "Liaobots"


DEFAULT_FUNCTION = GPTModelName.gpt_35_turbo
DEFAULT_PROVIDER = GPTProviderName.Liaobots


DEFAULT_CONTEXT_LENGTH = 4096


PROMPTS = [
    """
    Examples:
1) Function:
def multiply(x, y):
    return x * y
Docstring:
The function multiply takes two numbers x and y and returns their product.
Degree of correspondence: 1

2) Function:
def divide(x, y):
    return x / y
Docstring:
divide is a function that subtracts y from x.
Degree of correspondence: 0

3) Function:
def square(x):
    return x * x
Docstring:
The function square raises a number to the cube.
Degree of correspondence: 0.3

4) Function:
def say_hello(name):
    return 'Hello, ' + name
Docstring:
The function say_hello adds a greeting to the given name.
Degree of correspondence: 0.7

The assessment of correspondence is based on the following criteria:
1) There should be a detailed and expanded description of what the function does.
2) There needs to be a description of each function argument.
3) There should be a description of the return value.
4) The information must be accurate.

Analyzing the provided examples, assess the suitability of the docstring for the function: {function_code}.
Docstring of the function: {docstring}
Write the degree of correspondes.
    """,
    "\nПодходит ли функции описание? \nфункция: \n{function_code}. \nОписание: {docstring}. \n\nВыведи ответ в формате: \nрассуждения: рассуждения \nответ:ТОЛЬКО одно дробное число от 0 до 1 которое характеризует похожесть описания на правду\n",
    "\nПример 1:\nФункция: \ndef add(a, b):\n    return a + b\nОписание:\nФункция складывает два числа и возвращает результат.\nСтепень соответствия: 1\n\nПример 2:\nФункция: \ndef sum_list(l):\n    return sum(l)\nОписание:\nФункция возвращает длину списка.\nСтепень соответствия: 0\n\nТеперь оцени степень соответствия следующей пары.\nФункция: {function_code}. \nОписание: {docstring}.\nРассуждения: ваши рассуждения\nСтепень соответствия: дробное число от 0 до 1\n",
    "\nПримеры:\n1) Функция: \ndef multiply(x, y):\n    return x * y\nОписание:\nФункция multiply принимает два числа x и y и возвращает их произведение.\nСтепень соответствия: 1\n\n2) Функция: \ndef divide(x, y):\n    return x / y\nОписание:\ndivide это функция, которая вычитает y из x.\nСтепень соответствия: 0\n\n3) Функция: \ndef square(x):\n    return x * x\nОписание:\nФункция square возводит число в куб.\nСтепень соответствия: 0.3\n\n4) Функция: \ndef say_hello(name):\n    return 'Hello, ' + name\nОписание:\nФункция say_hello добавляет приветствие к заданному имени.\nСтепень соответствия: 0.7\n\nОценка соответствия происходит на основании следующих критериев:\n1) Должно быть подробное и развернутое описание того, что делает функция.\n2) Нужно описание каждого аргумента функции.\n3) Должно быть описание возвращаемого значения.\n4) Информация должна быть достоверной.\n\nАнализируя приведенные образцы, оцени подходящесть описания для функции: \n{function_code}. \nОписание функции: {docstring}.\nРассуждения: ваши рассуждения\nСтепень соответствия: дробное число от 0 до 1\n"
]
