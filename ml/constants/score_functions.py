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
Imagine, that you are my code assistant.    
I had a function and wrote a docstring for it. I need you to score it's correspondence by the following criteria.
The assessment of correspondence is based on the following criteria:
1) There should be a detailed and expanded description of what the function does.
2) There needs to be a description of each function argument.
3) There should be a description of the return value.
4) The information must be accurate.
I will give you the code of a function, docstring, then you must write your analysis and final score.
You must write score in format "Score: {value - float from 0 to 1}".

Examples:
Function:
def multiply(x, y):
    return x * y
Docstring:
The function multiply takes two numbers x and y and returns their product.
Analysis:
1) The docstring states that the function "takes two numbers x and y and returns their product". 
This is a clear and concise description of the function's purpose.
2) The docstring does not provide a description of each function argument.
3) The docstring does not provide a description of the return value.
4) The information in the docstring is accurate.
Score: 0.7

Function:
def divide(x, y):
    return x / y
Docstring:
divide is a function that subtracts y from x.
Analysis:
1) The docstring is missing a description of what the function actually does, which is dividing x by y.
2) The docstring does not describe the arguments x and y.
3) The docstring does not describe the return value
4)  The information in the docstring is inaccurate, as it states that the function subtracts y from x,
which is not what the function does.
Score: 0.2

Function:
def square(x):
    return x * x
Docstring:
The function square raises a number to the cube.
Analysis:
1) The docstring incorrectly states that the function raises a number to the cube, 
when it actually raises a number to the power of 2.
2) The docstring does not provide any description of the function argument x.
3) The docstring does not provide any description of the return value.
4) The information provided in the docstring is inaccurate, 
as it incorrectly states that the function raises a number to the cube.
Score: 0.2

Function:
def say_hello(name):
    return 'Hello, ' + name
Docstring:
Prints a greeting to the specified name.
    Args:
        name (str): The name of the person to greet.

    Returns:
        str: A greeting message.
Analysis:
1) The docstring states "Prints a greeting to the specified name", 
which is a clear and concise description of the function's purpose.
2) The docstring states "Args: name (str): The name of the person to greet.", 
which accurately describes the single function argument.
3) The docstring states "Returns: str: A greeting message.", which accurately describes the return value.
4) The docstring accurately describes the function's functionality, argument, and return value.
Score: 1.0

Now I need you to score my function, 
Function:
{function_code}
Docstring:
{docstring}

Now write your analysis and a score in format "Analysis: {your analysis}\nScore: {float from 0 to 1}"
Analysis:
    """,
]

TESTS_PROMPT = [
    """
Imagine, that you are my code assistant.    
I had a function and wrote unit-tests for it. I need you to score it by the following criteria.
The assessment of unit-tests is based on the following criteria:
1) Tests must be a correct Python code with no syntax mistakes
2) Tests must cover all corner cases of a function
You must write score in format "Score: {value - float from 0 to 1}".

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
Analysis:
1) These unit-tests is a correct Python code 
2) There unit-tests check all corner cases, to they are quite good
Score: 1.0

Function: 
{function_code}
Unit-tests:
{unit_test}

Now write your analysis and a score in format "Analysis: {your analysis}\nScore: {float from 0 to 1}"
Analysis:
    """,
]

SEMANTIC_PROMPTS = [
    """
    """
]
