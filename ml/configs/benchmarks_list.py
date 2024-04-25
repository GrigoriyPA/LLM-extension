from constants import extension as extension_constants
from configs import database as database_config
from src import base_benchmark as base_benchmark_config
from src import database_entities
from src import database_utils


DOCSTRING_BENCHMARK_V1: base_benchmark_config.Benchmark[database_entities.Function] = (
    base_benchmark_config.Benchmark[database_entities.Function](
        tables=[
            database_utils.Table(
                db=database_config.MAIN_DATABASE,
                table_name=database_config.GITHUB_DATASET_TABLE_NAME,
                row_type=database_entities.Function
            )
        ],
        feature=extension_constants.ExtensionFeature.docstring_generation,
        benchmark_name="DOCSTRING_BENCHMARK_V1",
    )
)