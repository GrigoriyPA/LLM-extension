from src.colourful_cmd import print_red
import typing as tp

from models.base_model import BaseModel
from datasets.database_utils import Dataset, get_tmp_dataset
from datasets.entities import Function
from score_function.score_function import ScoreFunction


async def test_models_on_docstring(models: tp.List[BaseModel],
                                   docstring_score_function: ScoreFunction,
                                   src: Dataset,
                                   dst: Dataset):
    labelled_dst: tp.List[Dataset] = []

    for model in models:
        try:
            dataset = src.read()
            tmp_src = get_tmp_dataset(Function)
            for function in dataset:
                function.docstring = model.generate_docstring(function)
                tmp_src.write(function)

            tmp_dst = await docstring_score_function.exec(src)
            model_results = tmp_dst.read()
            for model_result in model_results:
                model_result.model_name = model.model_name
                model_result.prompt = model.get_prompt_for_docstring_generation(model_result)
            labelled_dst.append(tmp_dst)

        except BaseException as e:
            print_red(f"Error while processing model {model.model_name}. Error: {e}")

    dst.write_datasets(labelled_dst)
