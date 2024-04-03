from benchmarks.docstrings import test_models_on_docstring
from datasets.entities import Function, ScorerModelDocstringResult
from configs.models_list import LanguageModel
from datasets.database_utils import Database, Dataset
from score_function.score_function import ScoreFunction

database = Database('data/github_data')
FUNCTION_DATASET = Dataset(database, "default_github_functions", Function)
MODELS_RESULTS_DATASET = Dataset(database, "models_results", ScorerModelDocstringResult)

models = [el.value for el in LanguageModel]

test_models_on_docstring(models, ScoreFunction(), FUNCTION_DATASET, MODELS_RESULTS_DATASET)
