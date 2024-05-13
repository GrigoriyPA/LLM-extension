import os

from src.database import database_utils

MAIN_DATABASE = database_utils.Database(os.getcwd() + "/data/main_database.db")
SCORER_RESULTS_ON_DATASET_TABLE_NAME = "score_last_result"
GITHUB_DATA_TABLE = 'default_github_functions'
FINETUNE_DOCSTRING_DATASET = 'finetune_docstring_dataset_night'

