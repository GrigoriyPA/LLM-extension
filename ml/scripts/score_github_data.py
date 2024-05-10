from src.constants import database as database_config
from configs import prompts
from src.scorers import base_scorer as base_scorer_config
from src.scorers import score_function as score_function_module
from src.database import database_entities
from src.database import database_utils

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
        prompt=prompts.SCORER_DOCSTRING_PROMPTS[0],
        scored_entity_type=database_entities.ScorerModelDocstringResult,
    ),
)

scores.score_data()
