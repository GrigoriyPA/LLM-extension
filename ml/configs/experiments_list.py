import typing as tp

from configs import benchmarks_list
from configs import prompts

from src.constants import language_models as language_models_constants
from src.constants import database as database_constants
from src.benchmarks import base_experiment
from src.scorers import score_function as score_function_module
from src.database import database_entities, database_utils

EXP_RESULT_TABLE = database_utils.Table(
    db=database_constants.MAIN_DATABASE,
    table_name="experiment_results",
    row_type=database_entities.ExperimentResult
)

DOCSTRING_EXPERIMENT_V1: base_experiment.Experiment[
    database_entities.Function,
    database_entities.ScorerModelDocstringResult
] = base_experiment.Experiment(
    exp_name="DOCSTRING_EXPERIMENT_V1",
    models=[el.value for el in language_models_constants.DocstringModels],
    score_function=score_function_module.ScoreFunction(
        prompt=prompts.SCORER_DOCSTRING_PROMPTS[0],
        scored_entity_type=database_entities.ScorerModelDocstringResult,
    ),
    benches=[benchmarks_list.DOCSTRING_BENCHMARK_V1],
    dst=EXP_RESULT_TABLE,
)

TEST_GENERATION_EXPERIMENT_V1: base_experiment.Experiment[
    database_entities.UnitTest,
    database_entities.ScorerModelUnitTestResult
] = base_experiment.Experiment(
    exp_name="TEST_GENERATION_EXPERIMENT_V1",
    models=[el.value for el in language_models_constants.TestGenerationModels],
    score_function=score_function_module.ScoreFunction(
        prompt=prompts.SCORER_TESTS_PROMPTS[0],
        scored_entity_type=database_entities.ScorerModelUnitTestResult,
    ),
    benches=[benchmarks_list.TEST_GENERATION_BENCHMARK_V1],
    dst=EXP_RESULT_TABLE,
)

DOCSTRING_EXPERIMENT_V1_CodeLlamas: base_experiment.Experiment[
    database_entities.Function,
    database_entities.ScorerModelDocstringResult
] = base_experiment.Experiment(
    exp_name="DOCSTRING_EXPERIMENT_V1_CodeLLama_8B",
    models=[
        language_models_constants.DocstringModels.codellama_instruct_7b.value,
        language_models_constants.DocstringModels.codellama_python_7b.value
    ],
    score_function=score_function_module.ScoreFunction(
        prompt=prompts.SCORER_DOCSTRING_PROMPTS[0],
        scored_entity_type=database_entities.ScorerModelDocstringResult,
    ),
    benches=[benchmarks_list.DOCSTRING_BENCHMARK_V1],
    dst=EXP_RESULT_TABLE,
)

EXPERIMENTS_LIST: tp.List[
    base_experiment.Experiment[
        database_entities.ENTITY_TYPE, database_entities.SCORED_ENTITY_TYPE
    ]
] = [
    # TEST_GENERATION_EXPERIMENT_V1,
    DOCSTRING_EXPERIMENT_V1,
]
