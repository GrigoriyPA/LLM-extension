from benchmarks.score_models import launch_models
from configs.models_names import LanguageModelName
from datasets.database_utils import Database, Dataset, FunctionDatasetRow, ModelsResultsRow

database = Database('datasets/main.db')
FUNCTION_DATASET = Dataset(database, "functions_docstrings", FunctionDatasetRow)
MODELS_RESULTS_DATASET = Dataset(database, "models_results", ModelsResultsRow)

models_names = [el.value for el in LanguageModelName]
launch_models(models_names, FUNCTION_DATASET, MODELS_RESULTS_DATASET)
