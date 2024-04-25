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



DEFAULT_FUNCTION = GPTModelName.llama3_70b_instruct
DEFAULT_PROVIDER = GPTProviderName.Llama


DEFAULT_CONTEXT_LENGTH = 4096
SLEEP_TIME_SEC = 60

DOCSTRING_PROMPTS = [
    """
    Examples:
1) Function:
def multiply(x, y):
    return x * y
Docstring:
The function multiply takes two numbers x and y and returns their product.
Score: 1

2) Function:
def divide(x, y):
    return x / y
Docstring:
divide is a function that subtracts y from x.
Score: 0

3) Function:
def square(x):
    return x * x
Docstring:
The function square raises a number to the cube.
Score: 0.3

4) Function:
def say_hello(name):
    return 'Hello, ' + name
Docstring:
The function say_hello adds a greeting to the given name.
Score: 0.7

The assessment of correspondence is based on the following criteria:
1) There should be a detailed and expanded description of what the function does.
2) There needs to be a description of each function argument.
3) There should be a description of the return value.
4) The information must be accurate.

Analyzing the provided examples, assess the suitability of the docstring for the function: {function_code}.
Docstring of the function: {docstring}
Write the analysis, and after that degree of correspondence in format "Score: "value - float from 0 to 1".
    """,
    "\nПодходит ли функции описание? \nфункция: \n{function_code}. \nОписание: {docstring}. \n\nВыведи ответ в формате: \nрассуждения: рассуждения \nответ:ТОЛЬКО одно дробное число от 0 до 1 которое характеризует похожесть описания на правду\n",
    "\nПример 1:\nФункция: \ndef add(a, b):\n    return a + b\nОписание:\nФункция складывает два числа и возвращает результат.\nСтепень соответствия: 1\n\nПример 2:\nФункция: \ndef sum_list(l):\n    return sum(l)\nОписание:\nФункция возвращает длину списка.\nСтепень соответствия: 0\n\nТеперь оцени степень соответствия следующей пары.\nФункция: {function_code}. \nОписание: {docstring}.\nРассуждения: ваши рассуждения\nСтепень соответствия: дробное число от 0 до 1\n",
    "\nПримеры:\n1) Функция: \ndef multiply(x, y):\n    return x * y\nОписание:\nФункция multiply принимает два числа x и y и возвращает их произведение.\nСтепень соответствия: 1\n\n2) Функция: \ndef divide(x, y):\n    return x / y\nОписание:\ndivide это функция, которая вычитает y из x.\nСтепень соответствия: 0\n\n3) Функция: \ndef square(x):\n    return x * x\nОписание:\nФункция square возводит число в куб.\nСтепень соответствия: 0.3\n\n4) Функция: \ndef say_hello(name):\n    return 'Hello, ' + name\nОписание:\nФункция say_hello добавляет приветствие к заданному имени.\nСтепень соответствия: 0.7\n\nОценка соответствия происходит на основании следующих критериев:\n1) Должно быть подробное и развернутое описание того, что делает функция.\n2) Нужно описание каждого аргумента функции.\n3) Должно быть описание возвращаемого значения.\n4) Информация должна быть достоверной.\n\nАнализируя приведенные образцы, оцени подходящесть описания для функции: \n{function_code}. \nОписание функции: {docstring}.\nРассуждения: ваши рассуждения\nСтепень соответствия: дробное число от 0 до 1\n"
]

TESTS_PROMPT = [
    """
Imagine, that you are my code assistant.    
I had a function and wrote unit-tests for it. I need you to score it by the following criteria.
The assessment of unit-tests is based on the following criteria:
1) Tests must be a correct Python code with no syntax mistakes
2) Tests must cover all corner cases of a function

Examples:
Function:
def pow(a, b):
    return a ** b
Unit-tests:
class TestPowFunction(unittest.TestCase):
    def test_positive_numbers(self):
        self.assertEqual(pow(2, 3), 8)
        self.assertEqual(pow(3, 2), 9)
        self.assertEqual(pow(5, 3), 125)

    def test_negative_exponent(self):
        self.assertEqual(pow(2, -2), 0.25)
        self.assertEqual(pow(4, -1), 0.25)
        
    def test_zero_exponent(self):
        self.assertEqual(pow(10, 0), 1)
        self.assertEqual(pow(0, 0), 1)  # Обычно 0**0 рассматривается как 1

    def test_zero_base(self):
        self.assertEqual(pow(0, 2), 0)
        self.assertEqual(pow(0, 10), 0)

    def test_fractional_exponent(self):
        self.assertAlmostEqual(pow(4, 0.5), 2)
        self.assertAlmostEqual(pow(9, 0.5), 3)
        self.assertAlmostEqual(pow(27, 1/3), 3)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            pow('two', 'five')

These unit-tests is a correct Python code and it checks all corner cases, to they are quite good
Score: 1.0

Function: 
{function_code}
Unit-tests:
{unit_test}
    """,
]
