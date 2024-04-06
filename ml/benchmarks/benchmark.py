import asyncio

from tqdm import tqdm

from configs.entities import ENTITY_TYPE, BenchmarkResult
from configs.main_config import ExtensionFeature
import typing as tp

from datasets.database_utils import Table, get_tmp_table
from models.base_model import BaseModel
from score_function.score_function import ScoreFunction
from src.colourful_cmd import print_red


class Benchmark(tp.Generic[ENTITY_TYPE]):
    def __init__(self, tables: tp.List[Table[ENTITY_TYPE]], feature: ExtensionFeature, benchmark_name: str):
        self.tables = tables
        self.feature = feature
        self.benchmark_name = benchmark_name

    def launch_models(self, models: tp.List[BaseModel]) -> tp.List[tp.Tuple[BaseModel, Table[ENTITY_TYPE]]]:
        result: tp.List[tp.Tuple[BaseModel, Table[ENTITY_TYPE]]] = []

        for model in tqdm(models):
            labelled_els: Table[ENTITY_TYPE] = get_tmp_table(type(ENTITY_TYPE))

            try:
                for table in self.tables:
                    els = table.read()
                    for el in tqdm(els):
                        el = el.set_prediction(model.get_method_for_extension_feature(self.feature)(el))
                        labelled_els.write(el)

            except BaseException as e:
                print_red(f"Error while processing model {model.model_name}. Error: {e}")

            result.append((model, labelled_els))

        return result

    def score_models(self, models: tp.List[BaseModel],
                     score_function: ScoreFunction,
                     dst: tp.Optional[Table[BenchmarkResult]] = None) -> tp.Dict[str, float]:
        models_predictions = self.launch_models(models)

        results: tp.Dict[str, float] = dict()
        for model, predictions in models_predictions:
            scored_predictions = asyncio.run(score_function.exec(predictions, model)).read()
            tmp = [el.get_prediction_score() for el in scored_predictions]
            results[model.model_name] = sum(tmp) / len(tmp)

            if dst:
                dst.write(BenchmarkResult(
                    model_name=model.model_name,
                    benchmark_name=self.benchmark_name,
                    feature=self.feature.value,
                    score=results[model.model_name],
                ))

        return results
