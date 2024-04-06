from __future__ import annotations

import abc
import typing as tp


class BaseEntity(tp.NamedTuple):
    @abc.abstractmethod
    def set_prediction(self, prediction: str) -> BaseEntity:
        """changes prediction field and returns modified object"""


class BaseScoredEntity(tp.NamedTuple):
    @abc.abstractmethod
    def get_prediction_score(self) -> str:
        """returns prediction score"""


ENTITY_TYPE = tp.TypeVar('ENTITY_TYPE', bound=BaseEntity)
SCORED_ENTITY_TYPE = tp.TypeVar('SCORED_ENTITY_TYPE', bound=BaseScoredEntity)


class Function(BaseEntity):
    function_name: str
    code: str
    docstring: str
    context: str

    def set_prediction(self, prediction):
        return self._replace(docstring=prediction)


class ScorerModelDocstringResult(BaseScoredEntity):
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


class ExperimentResult(tp.NamedTuple):
    models: str


import json

p = json.loads('[{"a": 1}]')
print(type(p))
