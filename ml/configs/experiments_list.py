from configs.benchmarks_list import DOCSTRING_BENCHMARK_V1
from src.entities import Function, ScorerModelDocstringResult, MAIN_DATABASE, ExperimentResult
from configs.models_config import LanguageModel
from configs.features_config import ExtensionFeature
from datasets.database_utils import Table
from experiments.base_experiment import Experiment
from score_function.score_function import ScoreFunction
from src.entities import ENTITY_TYPE, SCORED_ENTITY_TYPE
import typing as tp

DOCSTRING_EXPERIMENT_V1: Experiment[Function, ScorerModelDocstringResult] = Experiment(
    exp_name="DOCSTRING_EXPERIMENT_V1",
    models=[el.value for el in LanguageModel],
    feature=ExtensionFeature.docstring_generation,
    score_function=ScoreFunction(),
    benches=[DOCSTRING_BENCHMARK_V1],
    dst=Table(MAIN_DATABASE, "experiment_results", ExperimentResult)
)

DOCSTRING_EXPERIMENT_ONLY_API_MODELS: Experiment[Function, ScorerModelDocstringResult] = Experiment(
    exp_name="DOCSTRING_EXPERIMENT_ONLY_API_MODELS",
    models=[LanguageModel.codellama_python_7b.value,
            LanguageModel.codellama_python_70b.value,
            LanguageModel.wizard_coder_34b.value],
    feature=ExtensionFeature.docstring_generation,
    score_function=ScoreFunction(),
    benches=[DOCSTRING_BENCHMARK_V1],
    dst=Table(MAIN_DATABASE, "experiment_results", ExperimentResult)
)

EXPERIMENTS_LIST: tp.List[Experiment[ENTITY_TYPE, SCORED_ENTITY_TYPE]] = [
    DOCSTRING_EXPERIMENT_V1,
    DOCSTRING_EXPERIMENT_ONLY_API_MODELS,
]
