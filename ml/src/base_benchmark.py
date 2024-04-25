import asyncio

from tqdm import tqdm

from src import database_entities, score_function as score_function_module
from src.database_entities import ENTITY_TYPE
import typing as tp

from src import database_utils
from models import base_model as base_model_module


class Benchmark(tp.Generic[ENTITY_TYPE]):
    def __init__(
            self,
            tables: tp.List[database_utils.Table[ENTITY_TYPE]],
            benchmark_name: str
    ) -> None:
        self.tables = tables
        self.benchmark_name = benchmark_name

    def launch_models(
            self,
            models: tp.List[base_model_module.BaseModel]
    ) -> tp.List[tp.Tuple[base_model_module.BaseModel, database_utils.Table[ENTITY_TYPE]]]:
        result: tp.List[tp.Tuple[base_model_module.BaseModel, database_utils.Table[ENTITY_TYPE]]] = []

        for model in tqdm(models):
            labelled_elements: database_utils.Table[ENTITY_TYPE] = database_utils.create_new_table(
                row_type=self.tables[0].row_type,
                table_name=f'model_{model.database_name}_results'
            )

            progress_bar = tqdm(self.tables)
            for table in progress_bar:
                elements = table.read()
                for element in tqdm(elements):
                    element.set_prediction(
                        model.generate_result(element)
                    )
                    labelled_elements.write(element)
                progress_bar.set_description(
                    f"Processing model {model.model_name} on table {table.table_name}"
                )
            result.append((model, labelled_elements))

        return result

    def score_models(
            self,
            models: tp.List[base_model_module.BaseModel],
            score_function: score_function_module.ScoreFunction,
            dst: tp.Optional[database_utils.Table[database_entities.BenchmarkResult]] = None
    ) -> tp.Dict[str, float]:
        models_predictions = self.launch_models(models)

        if not dst:
            dst = database_utils.create_new_table(
                row_type=database_entities.BenchmarkResult,
                table_name=f'benchmark_{self.benchmark_name}_results'
            )

        results: tp.Dict[str, float] = dict()
        for model, predictions in models_predictions:
            scored_predictions = asyncio.run(score_function.exec(src=predictions, model=model)).read()
            tmp = [element.get_prediction_score() for element in scored_predictions]
            init_length = len(tmp)
            tmp = [element for element in tmp if element is not None]
            if len(tmp) != init_length:
                print('None scores amount is', init_length - len(tmp))
            results[model.model_name] = sum(tmp) / len(tmp)

            dst.write(database_entities.BenchmarkResult(
                model_name=model.model_name,
                benchmark_name=self.benchmark_name,
                score=results[model.model_name],
            ))

        return results
