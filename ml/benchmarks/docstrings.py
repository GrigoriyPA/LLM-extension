from src.colourful_cmd import print_red
import typing as tp
from tqdm import tqdm
import asyncio

from models.base_model import BaseModel
from datasets.database_utils import Dataset, get_tmp_dataset
from datasets.entities import Function, BenchmarkResult
from score_function.score_function import ScoreFunction


def test_models_on_docstring(models: tp.List[BaseModel],
                             docstring_score_function: ScoreFunction,
                             src: Dataset,
                             dst: Dataset):
    labelled_docstrings: tp.List[Dataset] = []

    for model in tqdm(models):
        try:
            dataset = src.read()
            tmp_src = get_tmp_dataset(Function)
            for function in tqdm(dataset):
                function = function._replace(docstring=model.generate_docstring(function))
                tmp_src.write(function)

            tmp_dst = asyncio.run(docstring_score_function.exec(tmp_src))
            model_results = tmp_dst.read()
            for i in tqdm(range(len(model_results))):
                model_results[i] = model_results[i]._replace(
                    model_name=model.model_name,
                    prompt=model.get_prompt_for_docstring_generation(model_results[i]),
                )
            tmp_dst.clear_and_write_many(model_results)
            labelled_docstrings.append(tmp_dst)

        except BaseException as e:
            print_red(f"Error while processing model {model.model_name}. Error: {e}")

    dst.write_datasets(labelled_docstrings)


def get_docstring_test_results(src: Dataset, dst: tp.Optional[Dataset] = None) -> tp.Dict[str, float]:
    results = dict()
    for el in src.read():
        results[el.model_name] = results.get(el.model_name, []) + [el.docstring_score]
    for key in results.keys():
        results[key] = sum(results[key]) / len(results[key])
        if dst:
            dst.write(BenchmarkResult(model_name=key, benchmark_name="docstring generation", score=results[key]))
    return results
