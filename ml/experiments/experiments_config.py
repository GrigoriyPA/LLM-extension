from benchmarks.benchmarks_config import DOCSTRING_BENCHMARK_V1
from configs.entities import Function, ScorerModelDocstringResult, MAIN_DATABASE, ExperimentResult
from configs.models_config import LanguageModel
from configs.features_config import ExtensionFeature
from datasets.database_utils import Table
from experiments.base_experiment import Experiment
from score_function.score_function import ScoreFunction

DOCSTRING_EXPERIMENT_V1: Experiment[Function, ScorerModelDocstringResult] = Experiment(
    exp_name="DOCSTRING_EXPERIMENT_V1",
    models=[el.value for el in LanguageModel],
    feature=ExtensionFeature.docstring_generation,
    score_function=ScoreFunction(),
    benches=[DOCSTRING_BENCHMARK_V1],
    dst=Table(MAIN_DATABASE, "experiment_results", ExperimentResult)
)

print(DOCSTRING_EXPERIMENT_V1.launch())
