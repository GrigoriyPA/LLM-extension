import json
from datetime import datetime
import typing as tp

from models import base_model
from src import base_benchmark, score_function as score_function_module
from src import database_entities
from src.database_entities import ENTITY_TYPE, SCORED_ENTITY_TYPE
from src import database_utils


class Experiment(tp.Generic[ENTITY_TYPE, SCORED_ENTITY_TYPE]):
    def __init__(
            self,
            exp_name: str,
            models: tp.List[base_model.BaseModel],
            score_function: score_function_module.ScoreFunction,
            benches: tp.List[base_benchmark.Benchmark],
            dst: database_utils.Table[database_entities.ExperimentResult]
    ) -> None:
        self.exp_name = exp_name
        self.models = models
        self.score_function = score_function
        self.benches = benches
        self.dst = dst
        self.start_time: tp.Optional[datetime] = None
        self.finish_time: tp.Optional[datetime] = None

    def launch(self) -> tp.Dict[str, tp.Dict[str, float]]:
        self.start_time = datetime.now()
        results: tp.Dict[str, tp.Dict[str, float]] = {}
        for bench in self.benches:
            scores = bench.score_models(
                models=self.models,
                score_function=self.score_function
            )
            results[bench.benchmark_name] = scores
        self.finish_time = datetime.now()

        self.dst.write(
            database_entities.ExperimentResult(
                exp_name=self.exp_name,
                models_names=json.dumps([el.model_name for el in self.models]),
                score_function=str(self.score_function),  # TODO
                benchmarks_results=json.dumps(results),
                start_time=self.start_time,
                finish_time=self.finish_time,
            )
        )

        return results
