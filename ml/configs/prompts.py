import textwrap

DOCSTRING_PROMPT = """Generate a docstring by the given declaration, 
definition (optional) and context (optional) of the function. 
Docstring must include detailed and extensive description of the function,
it's parameters and return value. 
Docstring must follow accurate format:
{a few sentences describing what function do}
{description of each argument}
{description of a return value}.
Here is the body of the function, 
for which you will have to write a docstring: """
DOCSTRING_PROMPT = DOCSTRING_PROMPT.replace("\n", " ")

TEST_GENERATION_PROMPT = ""

SEMANTIC_SENSE_PROMPT = ""

DOCSTRING_EXAMPLES = [
    textwrap.dedent("""
    def find_maximum(arr):
        max_el = -1
        for el in arr:
            max_el = max(max_el, el)
        return max_el
    ->
    Function find_maximum finds the biggest element in the list 
    
    Parameters
    ----------
    arr: list[int]
        List of numbers
    
    Returns
    -------
    int
        The maximum element from the array
        
    """),
]
