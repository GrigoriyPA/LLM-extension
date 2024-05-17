from src.constants import database as database_config
from src.benchmarks import base_benchmark
from src.database import database_entities, database_utils

DOCSTRING_BENCHMARK_V1: base_benchmark.Benchmark[database_entities.Function] = (
    base_benchmark.Benchmark[database_entities.Function](
        tables=[
            database_utils.Table(
                db=database_config.MAIN_DATABASE,
                table_name=database_config.GITHUB_DATA_TABLE,
                row_type=database_entities.Function
            )
        ],
        benchmark_name="docstring",
    )
)

DOCSTRING_BENCHMARK_V2_100_FUNCS: base_benchmark.Benchmark[database_entities.Function] = (
    base_benchmark.Benchmark[database_entities.Function](
        tables=[
            database_utils.Table(
                db=database_config.MAIN_DATABASE,
                table_name="benchmark_best_100_functions",
                row_type=database_entities.Function
            )
        ],
        benchmark_name="docstring_100_funcs",
    )
)

TEST_GENERATION_BENCHMARK_V1: base_benchmark.Benchmark[database_entities.Function] = (
    base_benchmark.Benchmark[database_entities.Function](
        tables=[
            database_utils.Table(
                db=database_config.MAIN_DATABASE,
                table_name='test_generation_data',
                row_type=database_entities.UnitTest
            )
        ],
        benchmark_name="test_generation",
    )
)
