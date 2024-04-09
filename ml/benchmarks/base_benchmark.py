import asyncio

from tqdm import tqdm

from src.entities import ENTITY_TYPE, BenchmarkResult
from configs.features_config import ExtensionFeature
import typing as tp

from datasets.database_utils import Table, get_tmp_table
from models.base_model import BaseModel
from score_function.score_function import ScoreFunction


class Benchmark(tp.Generic[ENTITY_TYPE]):
    def __init__(self, tables: tp.List[Table[ENTITY_TYPE]], feature: ExtensionFeature, benchmark_name: str):
        self.tables = tables
        self.feature = feature
        self.benchmark_name = benchmark_name

    def launch_models(self, models: tp.List[BaseModel]) -> tp.List[tp.Tuple[BaseModel, Table[ENTITY_TYPE]]]:
        result: tp.List[tp.Tuple[BaseModel, Table[ENTITY_TYPE]]] = []

        for model in tqdm(models):
            labelled_els: Table[ENTITY_TYPE] = get_tmp_table(self.tables[0].row_type)

            for table in self.tables:
                els = table.read()
                for el in tqdm(els):
                    el.set_prediction(model.get_method_for_extension_feature(self.feature)(el))
                    labelled_els.write(el)

            result.append((model, labelled_els))

        return result

    def score_models(self, models: tp.List[BaseModel],
                     score_function: ScoreFunction,
                     dst: tp.Optional[Table[BenchmarkResult]] = None) -> tp.Dict[str, float]:
        models_predictions = self.launch_models(models)

        if not dst:
            dst = get_tmp_table(BenchmarkResult, self.benchmark_name)

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
