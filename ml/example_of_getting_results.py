from datasets.database_utils import Database, Dataset
from datasets.entities import ModelDocstringResult
from benchmarks.docstrings import get_docstring_test_results

database = Database('data/github_data')
dataset = Dataset(database, "models_results", ModelDocstringResult)
print(get_docstring_test_results(dataset))
