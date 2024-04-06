import json
import typing as tp
from datetime import datetime

from benchmarks.base_benchmark import Benchmark
from configs.entities import ENTITY_TYPE, SCORED_ENTITY_TYPE, ExperimentResult
from configs.features_config import ExtensionFeature
from datasets.database_utils import Table
from models.base_model import BaseModel
from score_function.score_function import ScoreFunction


class Experiment(tp.Generic[ENTITY_TYPE, SCORED_ENTITY_TYPE]):
    def __init__(self, exp_name: str, models: tp.List[BaseModel], feature: ExtensionFeature,
                 score_function: ScoreFunction, benches: tp.List[Benchmark], dst: Table[ExperimentResult]):
        self.exp_name = exp_name
        self.models = models
        self.feature = feature
        self.score_function = score_function
        self.benches = benches
        self.dst = dst
        self.start_time: tp.Optional[datetime] = None
        self.finish_time: tp.Optional[datetime] = None

    def launch(self) -> tp.Dict[str, tp.Dict[str, float]]:
        self.start_time = datetime.now()
        results: tp.Dict[str, tp.Dict[str, float]] = {}
        for bench in self.benches:
            scores = bench.score_models(self.models, self.score_function)
            results[bench.benchmark_name] = scores
        self.finish_time = datetime.now()

        self.dst.write(
            ExperimentResult(
                exp_name=self.exp_name,
                models_names=json.dumps([el.model_name for el in self.models]),
                feature=self.feature.value,
                score_function=str(self.score_function),  # TODO
                benchmarks_results=json.dumps(results),
                start_time=self.start_time,
                finish_time=self.finish_time,
            )
        )

        return results
