from configs import database as database_config
from src import database_entities
from src import database_utils
from src import base_scorer as base_scorer_config
from src import score_function as score_function_module

src = [
    database_utils.Table(
        db=database_config.MAIN_DATABASE,
        table_name="default_github_functions",
        row_type=database_entities.Function
    )
]

scores = base_scorer_config.Scorer[database_entities.Function](
    src_tables=src, 
    score_function=score_function_module.ScoreFunction()
)

scores.score_data()
