import typing as tp

ENTITY_TYPE = tp.TypeVar('ENTITY_TYPE', bound=tp.NamedTuple)


class Function(tp.NamedTuple):
    function_name: str
    code: str
    docstring: str
    context: str

    def set_prediction(self, prediction):
        return self._replace(docstring=prediction)


class ScorerModelDocstringResult(tp.NamedTuple):
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

    def get_prediction_score(self):
        return self.docstring_score


class BenchmarkResult(tp.NamedTuple):
    model_name: str
    benchmark_name: str
    feature: str
    score: float
