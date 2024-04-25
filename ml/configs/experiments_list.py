import typing as tp

from configs import benchmarks_list, language_models
from configs import database as database_config

from constants import score_functions as score_functions_config

from experiments import base_experiment

from src import database_entities, score_function as score_function_module
from src import database_utils

DOCSTRING_EXPERIMENT_V1: base_experiment.Experiment[
    database_entities.Function,
    database_entities.ScorerModelDocstringResult
] = base_experiment.Experiment(
    exp_name="docstring",
    models=[el.value for el in language_models.DocstringModels],
    score_function=score_function_module.ScoreFunction(
        prompt=score_functions_config.DOCSTRING_PROMPTS[0],
        scored_entity_type=score_function_module.database_entities.ScorerModelDocstringResult,
    ),
    benches=[benchmarks_list.DOCSTRING_BENCHMARK_V1],
    dst=database_utils.Table(
        db=database_config.MAIN_DATABASE,
        table_name="experiment_results",
        row_type=database_entities.ExperimentResult
    )
)

DOCSTRING_EXPERIMENT_V2: base_experiment.Experiment[
    database_entities.Function,
    database_entities.ScorerModelDocstringResult
] = base_experiment.Experiment(
    exp_name="DOCSTRING_EXPERIMENT_V2",
    models=[language_models.DocstringModels.docstring_llama_model.value],
    score_function=score_function_module.ScoreFunction(
        prompt=score_functions_config.DOCSTRING_PROMPTS[0],
        scored_entity_type=score_function_module.database_entities.ScorerModelDocstringResult,
    ),
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

EXPERIMENTS_LIST2: tp.List[
    base_experiment.Experiment[
        database_entities.ENTITY_TYPE, database_entities.SCORED_ENTITY_TYPE
    ]
] = [
    DOCSTRING_EXPERIMENT_V2,
]