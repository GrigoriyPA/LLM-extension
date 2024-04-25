from configs import database as database_config
from constants import score_functions as score_functions_config
from src import database_entities, base_scorer as base_scorer_config, score_function as score_function_module
from src import database_utils

src = [
    database_utils.Table(
        db=database_config.MAIN_DATABASE,
        table_name=database_config.GITHUB_DATA_TABLE,
        row_type=database_entities.Function
    )
]

scores = base_scorer_config.Scorer[database_entities.Function](
    src_tables=src, 
    score_function=score_function_module.ScoreFunction(
        prompt=score_functions_config.DOCSTRING_PROMPTS[0],
        scored_entity_type=score_function_module.database_entities.ScorerModelDocstringResult,
    ),
)

scores.score_data()
