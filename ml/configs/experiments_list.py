import typing as tp

from constants import extension as extension_constants
from configs import benchmarks_list, language_models
from configs import database as database_config

from experiments import base_experiment

from src import database_entities
from src import database_utils
from src import score_function as score_function_module

DOCSTRING_EXPERIMENT_V1: base_experiment.Experiment[
    database_entities.Function,
    database_entities.ScorerModelDocstringResult
] = base_experiment.Experiment(
    exp_name="DOCSTRING_EXPERIMENT_V1",
    models=[el.value for el in language_models.LanguageModel],
    feature=extension_constants.ExtensionFeature.docstring_generation,
    score_function=score_function_module.ScoreFunction(),
    benches=[benchmarks_list.DOCSTRING_BENCHMARK_V1],
    dst=database_utils.Table(
        db=database_config.MAIN_DATABASE,
        table_name="experiment_results",
        row_type=database_entities.ExperimentResult
    )
)

EXPERIMENTS_LIST: tp.List[
    base_experiment.Experiment[
        database_entities.ENTITY_TYPE, database_entities.SCORED_ENTITY_TYPE
    ]
] = [
    DOCSTRING_EXPERIMENT_V1,
]
