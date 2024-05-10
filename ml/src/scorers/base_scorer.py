import asyncio
from datetime import datetime
import typing as tp

from src.scorers import score_function as score_function_module
from src.database import database_entities, database_utils
from src.database.database_entities import SCORED_ENTITY_TYPE
from tqdm import tqdm
from src.constants import database as database_constants


class Scorer(tp.Generic[SCORED_ENTITY_TYPE]):
    def __init__(
            self,
            src_tables: tp.List[
                database_utils.Table[database_entities.ENTITY_TYPE]
            ],
            score_function: score_function_module.ScoreFunction,
    ) -> None:
        self.src_tables = src_tables
        self.score_function = score_function
        self.start_time: tp.Optional[datetime] = None
        self.finish_time: tp.Optional[datetime] = None
    
    def score_data(
            self,
    ) -> tp.List[database_utils.Table[database_entities.ENTITY_TYPE]]:
        result: tp.List[
            database_utils.Table[database_entities.ENTITY_TYPE]
        ] = []
        progress_bar = tqdm(self.src_tables)
        
        for table in progress_bar:
            dst: database_utils.Table[
                database_entities.ScorerModelDocstringResult
            ] = database_utils.create_new_table(
                database_constants.MAIN_DATABASE,
                row_type=database_entities.ScorerModelDocstringResult,
                table_name=(
                    database_constants.SCORER_RESULTS_ON_DATASET_TABLE_NAME
                )
            )
            asyncio.run(
                self.score_function.exec(
                    src=table, dst=dst, debug=True, start_index=0
                )
            )
            progress_bar.set_description(
                f"Processing scorer on table {table.table_name}"
            )
            result.append(dst)
        return result
