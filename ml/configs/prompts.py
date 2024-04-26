DOCSTRING_PROMPT = """Generate a docstring by the given declaration, 
definition (optional) and context (optional) of the function. 
Docstring must include detailed and extensive description of the function,
it's parameters and return value. 
Docstring must follow accurate format:
"a few sentences describing what function do"
"description of each argument"
"description of a return value".
Here is the body of the function, 
for which you will have to write a docstring: 
{code}
{context_info}
Docstring for that function:"""
DOCSTRING_PROMPT = DOCSTRING_PROMPT.replace("\n", " ")

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
print(f"You are only {user_age} years old, so you are not allowed to proceed")
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
