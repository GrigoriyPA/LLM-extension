from benchmarks.base_benchmark import Benchmark
from src.entities import Function, MAIN_DATABASE
from configs.features_config import ExtensionFeature
from datasets.database_utils import Table

DOCSTRING_BENCHMARK_V1: Benchmark[Function] = Benchmark[Function](
    tables=[Table(MAIN_DATABASE, "default_github_functions", Function)],
    feature=ExtensionFeature.docstring_generation,
    benchmark_name="DOCSTRING_BENCHMARK_V1",
)
