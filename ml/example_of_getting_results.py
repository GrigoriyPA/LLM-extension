from datasets.database_utils import Database, Dataset
from datasets.entities import ScorerModelDocstringResult
from benchmarks.docstrings import get_docstring_test_results

database = Database('data/github_data')
dataset = Dataset(database, "models_results", ScorerModelDocstringResult)
print(get_docstring_test_results(dataset))
