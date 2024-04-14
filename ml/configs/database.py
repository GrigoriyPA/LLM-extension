import os

from src import database_utils

MAIN_DATABASE = database_utils.Database(os.getcwd() + "/data/main_database.db")
