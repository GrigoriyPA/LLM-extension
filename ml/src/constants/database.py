import os

from src.database import database_utils

MAIN_DATABASE = database_utils.Database(os.getcwd() + "/data/main_database.db")
SCORER_RESULTS_ON_DATASET_TABLE_NAME = "score_last_result"
GITHUB_DATA_TABLE = 'default_github_functions'
GITHUB_DATA_VARIABLES_TABLE = 'default_github_semantic_sense'
FINETUNE_DOCSTRING_DATASET = 'finetune_docstring_dataset_night'

