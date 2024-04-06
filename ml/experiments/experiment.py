import typing as tp
from datetime import datetime

from benchmarks.benchmark import Benchmark
from configs.entities import ENTITY_TYPE, SCORED_ENTITY_TYPE, ExperimentResult
from configs.main_config import ExtensionFeature
from datasets.database_utils import Table
from models.base_model import BaseModel
from score_function.score_function import ScoreFunction


class Experiment(tp.Generic[ENTITY_TYPE, SCORED_ENTITY_TYPE]):
    def __init__(self, models: tp.List[BaseModel], task_type: ExtensionFeature, score_function: ScoreFunction,
                 benches: tp.List[Benchmark], dst: Table[ExperimentResult]):
        self.models = models
        self.task_type = task_type
        self.score_function = score_function
        self.benches = benches
        self.dst = dst
        self.creation_time = datetime.now()
