from configs import database as database_config
from src import base_benchmark
from src import database_entities
from src import database_utils


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
