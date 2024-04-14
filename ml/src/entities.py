from __future__ import annotations

import abc
import typing as tp
import datetime
import os

from datasets.database_utils import Database

MAIN_DATABASE = Database(os.getcwd() + "/data/main_database.db")


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
    docstring: str
    context: str

    def __new__(cls, function_name: str, code: str, docstring: str, context: str):
        self = super(Function, cls).__new__(cls)
        self.function_name = function_name
        self.code = code
        self.docstring = docstring
        self.context = context
        return self

    def set_prediction(self, prediction) -> None:
        self.docstring = prediction


class ScorerModelDocstringResult(Function, BaseScoredEntity):
    model_name: str
    prompt: str
    scorer_prompt: str
    docstring_score: float
    scorer_response: str

    def __new__(cls, function_name: str, code: str, docstring: str, context: str, model_name: str,
                prompt: str, scorer_prompt: str, docstring_score: float, scorer_response: str):
        self = super(ScorerModelDocstringResult, cls).__new__(cls, function_name, code, docstring, context)
        self.model_name = model_name
        self.prompt = prompt
        self.scorer_prompt = scorer_prompt
        self.docstring_score = docstring_score
        self.scorer_response = scorer_response
        return self

    def get_prediction_score(self) -> float:
        return self.docstring_score


class BenchmarkResult(tp.NamedTuple):
    model_name: str
    benchmark_name: str
    feature: str
    score: float


class ExperimentResult(tp.NamedTuple):
    exp_name: str
    models_names: str  # use json
    feature: str
    score_function: str
    benchmarks_results: str  # use json
    start_time: datetime.datetime
    finish_time: datetime.datetime
