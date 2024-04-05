from datasets.database_utils import Database, Table
from configs.entities import ScorerModelDocstringResult
from benchmarks.docstrings import get_docstring_test_results

database = Database('data/github_data')
dataset = Table(database, "models_results", ScorerModelDocstringResult)
print(get_docstring_test_results(dataset))
