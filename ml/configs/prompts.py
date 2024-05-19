DOCSTRING_PROMPT = """Generate only a docstring by the given declaration, 
definition (optional) and context (optional) of the function. Start your docstring with \"\"\" and end with \"\"\".
Docstring must include detailed and extensive description of the function,
it's parameters and return value. 
Docstring must follow accurate format:
"a few sentences describing what function do"
"description of each argument"
"description of a return value".
Here is the body of the function, 
for which you will have to write a docstring: 
{code}
Write only docstring for that function:"""
DOCSTRING_PROMPT = DOCSTRING_PROMPT.replace("\n", " ")

FINETUNE_DOCSTRING_PROMPT = "Function:\n{code}\nDocstring:"

SHORT_DOCSTRING_PROMPT = """Write docstring for a function. 
Function:
{code}
Docstring:
"""

FEWSHOT_DOCSTRING_PROMPT = """Write docstring for a function. 
Docstring must include detailed and extensive description of the function,
it's parameters and return value. 

Examples:

Function:
def make_causal_mask(
  x: Array, extra_batch_dims: int = 0, dtype: Dtype = jnp.float32
) -> Array:
    idxs = jnp.broadcast_to(jnp.arange(x.shape[-1], dtype=jnp.int32), x.shape)
    return make_attention_mask(
    idxs,
    idxs,
    jnp.greater_equal,
    extra_batch_dims=extra_batch_dims,
    dtype=dtype,
    )
Docstring:
Create a causal attention mask.

Args:
x: The input tensor.
extra_batch_dims: The number of extra batch dimensions.
dtype: The data type of the output mask.

Returns:
A causal attention mask.

Function:
def url_for(
    endpoint: str,
    *,
    _anchor: str | None = None,
    _method: str | None = None,
    _scheme: str | None = None,
    _external: bool | None = None,
    **values: t.Any,
) -> str:
    return current_app.url_for(
        endpoint,
        _anchor=_anchor,
        _method=_method,
        _scheme=_scheme,
        _external=_external,
        **values,
    )
Docstring:
Generate a URL to a specific endpoint.

    This function is similar to the Werkzeug url_for function, but it uses
    the current Flask application's URL map.

    Args:
        endpoint: The name of the endpoint to generate a URL for.
        _anchor: An optional anchor to append to the URL.
        _method: An optional HTTP method to use for the URL.
        _scheme: An optional scheme to use for the URL.
        _external: An optional boolean indicating whether the URL should
            be absolute or relative.
        values: Any additional key/value pairs to include in the URL.

    Returns:
        A string containing the generated URL.

Function:
def do_teardown_request(
    self,
    exc: BaseException | None = _sentinel,      ) -> None:
    if exc is _sentinel:
        exc = sys.exc_info()[1]

    for name in chain(request.blueprints, (None,)):
        if name in self.teardown_request_funcs:
            for func in reversed(self.teardown_request_funcs[name]):
                self.ensure_sync(func)(exc)

    request_tearing_down.send(self, _async_wrapper=self.ensure_sync, exc=exc)
Docstring:
Execute teardown functions.

        This method is called at the end of the request, after the response has
        been sent.  It executes all teardown functions registered for the
        current blueprint and application.

        Args:
            exc: An optional exception that caused the request to fail.

Function:
{code}
Docstring:
"""

TEST_GENERATION_PROMPT = """Write unit-tests for the given function

Examples:
Function:
def pow(a, b):
    return a ** b
Unittests:
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


Function:
{code}
Unittests:
"""

SEMANTIC_SENSE_PROMPT = """Write semantic sense for the given variable names and it's usages
Examples:

Variable name:
user_age
Usages:
user_age = int(input())
if user_age < 18:
if user_age > 100:
print(f"You are only user_age years old, so you are not allowed to proceed")
Semantic Sense:
The variable user_age represents the age of a user. It is used to:

• Store the user's age as an integer.
• Check if the user is under 18 years old.
• Check if the user is over 100 years old.
• Print a message to the user based on their age.

Variable name:
{variable_name}
Usages:
{context}
Semantic Sense:
"""

EMPTY_AUTOCOMPLETE_PROMPT = "{code}"

SHORT_AUTOCOMPLETE_PROMPT = "Continue that code:\n{code}"

AUTOCOMPLETE_PROMPT = """
    Imagine, that you are my code assistant. I need you to complete the following code.
    Be careful, don't use undeclared variables. If you do great, I will pay you 500 dollars.
    Predict only a few words, that would fit best. Now here is the code: {code}
""".replace("\n", " ")

# scorer model prompts:

SCORER_DOCSTRING_PROMPTS = [
    """
Imagine, that you are my code assistant.    
I had a function and wrote a docstring for it. I need you to score it's correspondence by the following criteria.
The assessment of correspondence is based on the following criteria:
1) There should be a detailed and expanded description of what the function does.
2) There needs to be a description of each function argument.
3) There should be a description of the return value.
4) The information must be accurate.
I will give you the code of a function, docstring, then you must write your analysis and final score.
You must write score in format "Score: "value - float from 0 to 1"".

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
{code}
Docstring:
{docstring}

Now write your analysis and a score in format "Analysis: "your analysis"\nScore: "float from 0 to 1""
Analysis:
    """,
]

SCORER_TESTS_PROMPTS = [
    """
Imagine, that you are my code assistant.    
I had a function and wrote unit-tests for it. I need you to score it by the following criteria.
The assessment of unit-tests is based on the following criteria:
1) Tests must be a correct Python code with no syntax mistakes
2) Tests must cover all corner cases of a function
You must write score in format "Score: "value - float from 0 to 1"".

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
2) These unit-tests check all corner cases, to they are quite good
Score: 1.0

Function: 
{code}
Unit-tests:
{unit_test}

Now write your analysis and a score in format "Analysis: "your analysis"\nScore: "float from 0 to 1""
Analysis:
    """,
]

SCORER_SEMANTIC_SENSE_PROMPTS = [
    """
Imagine, that you are my code assistant.    
I had a variable or a function and wrote description of what it's semantic sense is. 
I need you to score it by the following criteria.
1) Semantic sense must be accurate
2) Semantic sense must mention all possible usages of a variable or a function based on the examples of usages
You must write score in format "Score: "value - float from 0 to 1"".

Examples:
Variable name:
user_age
Usages:
user_age = int(input())
if user_age < 18:
if user_age > 100:
print(f"You are only user_age years old, so you are not allowed to proceed")
Semantic Sense:
The variable user_age represents the age of a user. It is used to:
• Store the user's age as an integer.
• Check if the user is under 18 years old.
• Check if the user is over 100 years old.
• Print a message to the user based on their age.
Analysis:
1) Semantic sense is accurate, it is absolutely true
2) Semantic sense mentions all usages
Score: 1.0
--end of examples

Now write your analysis for this:

Variable name: 
{variable_name}
Usages:
{context}
Semantic Sense:
{semantic_sense}

Now write your analysis and a score in format "Analysis: "your analysis"\nScore: "float from 0 to 1""
Analysis:
    """,
]


