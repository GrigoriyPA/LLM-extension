import typing as tp


class Function(tp.NamedTuple):
    function_name: str
    code: str
    docstring: str
    context: str


class ModelDocstringResult(tp.NamedTuple):
    # from Function
    function_name: str
    code: str
    docstring: str
    context: str

    # new fields
    model_name: str
    prompt: str
    scorer_prompt: str
    docstring_score: float
    scorer_response: str


class BenchmarkResult(tp.NamedTuple):
    model_name: str
    benchmark_name: str
    score: float
