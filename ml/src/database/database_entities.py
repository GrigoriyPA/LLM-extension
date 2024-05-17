from __future__ import annotations

import abc
import datetime
import typing as tp


class BaseEntity(tp.NamedTuple):
    @abc.abstractmethod
    def set_prediction(self, prediction: str) -> None:
        """changes prediction field"""


class BaseScoredEntity(tp.NamedTuple):
    @abc.abstractmethod
    def get_prediction_score(self) -> float:
        """returns prediction score"""


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
            unit_test: tp.Optional[str] = None
    ):
        self = super(Function, cls).__new__(cls)
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
    ):
        self = super(BaseEntity, cls).__new__(cls)
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

    def __new__(cls, variable_name: str, context: str, semantic_sense: str):
        self = super(BaseEntity, cls).__new__(cls)
        self.variable_name = variable_name
        self.context = context
        self.semantic_sense = semantic_sense
        return self

    def set_prediction(self, prediction) -> None:
        self.semantic_sense = prediction


class AutoComplete(BaseEntity):
    code: str
    autocomplete: str

    def __new__(cls, code: str, autocomplete: str):
        self = super(BaseEntity, cls).__new__(cls)
        self.code = code
        self.autocomplete = autocomplete
        return self

    def set_prediction(self, prediction) -> None:
        self.autocomplete = prediction


class ScorerModelDocstringResult(Function, BaseScoredEntity):
    model_name: str
    prompt: str
    scorer_prompt: str
    docstring_score: float
    scorer_response: str

    def __new__(
            cls,
            function_name: str,
            code: str,
            docstring: str,
            context: str,
            unit_test: str,
            model_name: str,
            prompt: str,
            scorer_prompt: str,
            docstring_score: float,
            scorer_response: str,
            *args,
            **kwargs
    ):
        self = super(
            ScorerModelDocstringResult,
            cls
        ).__new__(
            cls,
            function_name=function_name,
            code=code,
            docstring=docstring,
            context=context
        )
        self.model_name = model_name
        self.prompt = prompt
        self.scorer_prompt = scorer_prompt
        self.docstring_score = docstring_score
        self.scorer_response = scorer_response
        return self

    def get_prediction_score(self) -> float:
        return self.docstring_score


class ScorerModelUnitTestResult(UnitTest, BaseScoredEntity):
    model_name: str
    prompt: str
    scorer_prompt: str
    unittest_score: float
    scorer_response: str

    def __new__(
            cls,
            function_name: str,
            code: str,
            context: tp.Optional[str],
            unit_test: tp.Optional[str],
            previous_test: tp.Optional[str],
            previous_stacktrace: tp.Optional[str],
            model_name: str,
            prompt: str,
            scorer_prompt: str,
            unittest_score: float,
            scorer_response: str,
            *args,
            **kwargs
    ):
        self = super(
            ScorerModelUnitTestResult, cls
        ).__new__(
            cls,
            function_name=function_name,
            code=code,
            context=context,
            unit_test=unit_test,
            previous_test=previous_test,
            previous_stacktrace=previous_stacktrace
        )
        self.model_name = model_name
        self.prompt = prompt
        self.scorer_prompt = scorer_prompt
        self.unittest_score = unittest_score
        self.scorer_response = scorer_response
        return self

    def get_prediction_score(self) -> float:
        return self.unittest_score


class ScorerModelSemanticSenseResult(SemanticSense, BaseScoredEntity):
    model_name: str
    prompt: str
    scorer_prompt: str
    semantic_sense_score: float
    scorer_response: str

    def __new__(
            cls,
            variable_name: str,
            context: str,
            semantic_sense: str,
            model_name: str,
            prompt: str,
            scorer_prompt: str,
            semantic_sense_score: float,
            scorer_response: str,
            *args,
            **kwargs
    ):
        self = super(
            ScorerModelSemanticSenseResult, cls
        ).__new__(
            cls,
            variable_name=variable_name,
            context=context,
            semantic_sense=semantic_sense
        )
        self.model_name = model_name
        self.prompt = prompt
        self.scorer_prompt = scorer_prompt
        self.semantic_sense_score = semantic_sense_score
        self.scorer_response = scorer_response
        return self

    def get_prediction_score(self) -> float:
        return self.semantic_sense_score


class ScorerModelAutoCompleteResult(AutoComplete, BaseScoredEntity):
    model_name: str
    prompt: str
    scorer_prompt: str
    autocomplete_score: float
    scorer_response: str

    def __new__(
            cls,
            code: str,
            autocomplete: str,
            model_name: str,
            prompt: str,
            scorer_prompt: str,
            autocomplete_score: float,
            scorer_response: str,
            *args,
            **kwargs
    ):
        self = super(
            ScorerModelAutoCompleteResult, cls
        ).__new__(
            cls,
            code=code,
            autocomplete=autocomplete,
        )
        self.model_name = model_name
        self.prompt = prompt
        self.scorer_prompt = scorer_prompt
        self.autocomplete_score = autocomplete_score
        self.scorer_response = scorer_response
        return self

    def get_prediction_score(self) -> float:
        return self.autocomplete_score


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
