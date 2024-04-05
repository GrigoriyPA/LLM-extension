from src.colourful_cmd import print_red
import typing as tp
from tqdm import tqdm
import asyncio

from models.base_model import BaseModel
from datasets.database_utils import Table, get_tmp_table
from configs.entities import Function, BenchmarkResult, ScorerModelDocstringResult
from score_function.score_function import ScoreFunction


def get_docstring_test_results(src: Table[ScorerModelDocstringResult],
                               dst: tp.Optional[Table[BenchmarkResult]] = None) -> tp.Dict[str, float]:
    scores: tp.Dict[str, tp.List[float]] = dict()
    for el in src.read():
        scores[el.model_name] = scores.get(el.model_name, []) + [el.docstring_score]

    results: tp.Dict[str, float] = dict()
    for key in results.keys():
        results[key] = sum(scores[key]) / len(scores[key])
        if dst:
            dst.write(BenchmarkResult(model_name=key, benchmark_name="docstring generation", score=results[key]))

    return results
