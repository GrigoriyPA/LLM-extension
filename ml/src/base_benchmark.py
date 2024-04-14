import asyncio

from tqdm import tqdm

from src.database_entities import ENTITY_TYPE, BenchmarkResult
from constants import extension as extension_constants
import typing as tp

from src import database_utils
from models import base_model as base_model_module
from src import score_function as score_function_module


class Benchmark(tp.Generic[ENTITY_TYPE]):
    def __init__(
            self,
            tables: tp.List[database_utils.Table[ENTITY_TYPE]],
            feature: extension_constants.ExtensionFeature,
            benchmark_name: str
    ) -> None:
        self.tables = tables
        self.feature = feature
        self.benchmark_name = benchmark_name

    def launch_models(
            self,
            models: tp.List[base_model_module.BaseModel]
    ) -> tp.List[tp.Tuple[base_model_module.BaseModel, database_utils.Table[ENTITY_TYPE]]]:
        result: tp.List[tp.Tuple[base_model_module.BaseModel, database_utils.Table[ENTITY_TYPE]]] = []

        for model in tqdm(models):
            labelled_els: database_utils.Table[ENTITY_TYPE] = database_utils.get_tmp_table(self.tables[0].row_type)

            pbar = tqdm(self.tables)
            for table in pbar:
                els = table.read()
                for el in tqdm(els):
                    el.set_prediction(model.get_method_for_extension_feature(self.feature)(el))
                    labelled_els.write(el)
                pbar.set_description(f"Processing model {model.model_name} on table {table.table_name}")
            result.append((model, labelled_els))

        return result

    def score_models(self, models: tp.List[base_model_module.BaseModel],
                     score_function: score_function_module.ScoreFunction,
                     dst: tp.Optional[database_utils.Table[BenchmarkResult]] = None) -> tp.Dict[str, float]:
        models_predictions = self.launch_models(models)

        if not dst:
            dst = database_utils.get_tmp_table(BenchmarkResult, self.benchmark_name)

        results: tp.Dict[str, float] = dict()
        for model, predictions in models_predictions:
            scored_predictions = asyncio.run(score_function.exec(predictions, model)).read()
            tmp = [el.get_prediction_score() for el in scored_predictions]
            init_length = len(tmp)
            tmp = [el for el in tmp if el is not None]
            if len(tmp) != init_length:
                print('None scores amount is', init_length - len(tmp))
            results[model.model_name] = sum(tmp) / len(tmp)

            dst.write(BenchmarkResult(
                model_name=model.model_name,
                benchmark_name=self.benchmark_name,
                feature=self.feature.value,
                score=results[model.model_name],
            ))

        return results
