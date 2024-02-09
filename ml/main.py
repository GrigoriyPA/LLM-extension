from benchmarks.score_models import launch_models
from configs.models_names import LanguageModelName
from datasets.database_utils import FunctionsDataset, ModelsResultsDataset, BaseDatabase

db = BaseDatabase('datasets/main.db')
src = FunctionsDataset(db)
dst = ModelsResultsDataset(db)

models_names = [el.value for el in LanguageModelName]

launch_models(models_names, src, dst)
