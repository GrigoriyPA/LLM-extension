from __future__ import annotations

import abc
import datetime
import typing as tp


class BaseEntity(tp.NamedTuple):
    @abc.abstractmethod
    def set_prediction(self, prediction: str) -> None:
        """changes prediction field"""


class BaseScoredEntity(tp.NamedTuple):
    model_name: str
    prompt: str
    scorer_prompt: str
    score: float
    scorer_response: str


ENTITY_TYPE = tp.TypeVar('ENTITY_TYPE', bound=BaseEntity)
SCORED_ENTITY_TYPE = tp.TypeVar('SCORED_ENTITY_TYPE', bound=BaseScoredEntity)


class Function(BaseEntity):
    function_name: str
    code: str
    docstring: tp.Optional[str]
    context: tp.Optional[str]
    unit_test: tp.Optional[str]

    def __new__(
            cls,
            function_name: str,
            code: str,
            docstring: tp.Optional[str] = None,
            context: tp.Optional[str] = None,
            unit_test: tp.Optional[str] = None,
            **kwargs
    ):
        self = super(Function, cls).__new__(cls, **kwargs)
        self.function_name = function_name
        self.code = code
        self.docstring = docstring
        self.context = context
        self.unit_test = unit_test
        return self

    def set_prediction(self, prediction) -> None:
        self.docstring = prediction


class UnitTest(BaseEntity):
    function_name: str
    code: str
    context: tp.Optional[str]
    unit_test: tp.Optional[str]
    previous_test: tp.Optional[str]
    previous_stacktrace: tp.Optional[str]

    def __new__(
            cls,
            function_name: str,
            code: str,
            context: tp.Optional[str] = None,
            unit_test: tp.Optional[str] = None,
            previous_test: tp.Optional[str] = None,
            previous_stacktrace: tp.Optional[str] = None,
            **kwargs
    ):
        self = super(BaseEntity, cls).__new__(cls, **kwargs)
        self.function_name = function_name
        self.code = code
        self.context = context
        self.unit_test = unit_test
        self.previous_test = previous_test
        self.previous_stacktrace = previous_stacktrace
        return self

    def set_prediction(self, prediction) -> None:
        self.unit_test = prediction


class SemanticSense(BaseEntity):
    variable_name: str
    context: str
    semantic_sense: str

    def __new__(
            cls,
            variable_name: str,
            context: str,
            semantic_sense: tp.Optional[str] = None,
            **kwargs
    ):
        self = super(BaseEntity, cls).__new__(cls, **kwargs)
        self.variable_name = variable_name
        self.context = context
        self.semantic_sense = semantic_sense
        return self

    def set_prediction(self, prediction) -> None:
        self.semantic_sense = prediction


class AutoComplete(BaseEntity):
    code: str
    autocomplete: tp.Optional[str]

    def __new__(
            cls,
            code: str,
            autocomplete: tp.Optional[str] = None,
            **kwargs
    ):
        self = super(BaseEntity, cls).__new__(cls, **kwargs)
        self.code = code
        self.autocomplete = autocomplete
        return self

    def set_prediction(self, prediction) -> None:
        self.autocomplete = prediction


class ScorerModelDocstringResult(Function, BaseScoredEntity):
    def __new__(
            cls,
            **kwargs
    ):
        return super().__new__(cls, **kwargs)


class ScorerModelUnitTestResult(UnitTest, BaseScoredEntity):
    def __new__(
            cls,
            **kwargs
    ):
        return super().__new__(cls, **kwargs)


class ScorerModelSemanticSenseResult(SemanticSense, BaseScoredEntity):
    def __new__(
            cls,
            **kwargs
    ):
        return super().__new__(cls, **kwargs)


class ScorerModelAutoCompleteResult(AutoComplete, BaseScoredEntity):
    def __new__(
            cls,
            **kwargs
    ):
        return super().__new__(cls, **kwargs)


class BenchmarkResult(tp.NamedTuple):
    benchmark_name: str
    model_name: str
    model_prompt: str
    score_model_name: str
    score_model_prompt: str
    score: float


class ExperimentResult(tp.NamedTuple):
    exp_name: str
    models_names: str  # use json
    score_function: str
    benchmarks_results: str  # use json
    start_time: datetime.datetime
    finish_time: datetime.datetime
