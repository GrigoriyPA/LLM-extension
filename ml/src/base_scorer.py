import asyncio
import json
from datetime import datetime
import typing as tp

from constants import extension
from models import base_model
from src import base_benchmark
from src import database_entities
from src import database_utils
from src import score_function
from models import base_model as base_model_module
from src import score_function as score_function_module
from tqdm import tqdm


class Scorer(tp.Generic[database_entities.SCORED_ENTITY_TYPE]):
    def __init__(
            self,
            src_tables: tp.List[database_utils.Table[database_entities.ENTITY_TYPE]],
            score_function: score_function.ScoreFunction,
    ) -> None:
        self.src_tables = src_tables
        self.score_function = score_function
        self.start_time: tp.Optional[datetime] = None
        self.finish_time: tp.Optional[datetime] = None
    
    def score_data(
            self,
    ) -> tp.List[database_utils.Table[database_entities.ENTITY_TYPE]]:
        result: tp.List[database_utils.Table[database_entities.ENTITY_TYPE]] = []
        progress_bar = tqdm(self.src_tables)
        
        for table in progress_bar:
            labelled_elements: database_utils.Table[database_entities.ScorerModelDocstringResult] = database_utils.create_new_table(
                row_type=database_entities.ScorerModelDocstringResult,
                table_name=f'scorer_{table.table_name}_results'
            )
            asyncio.run(self.score_function.exec(src=table, dst=labelled_elements))
            progress_bar.set_description(
                f"Processing scorer on table {table.table_name}"
            )
        result.append(labelled_elements)
        return result