import time

from configs.colourful_cmd import *
from models.models import IdeLLM

from typing import List


def _get_model_prediction(model, model_name, dst, function, context=""):
    res = model.generate_docstring(function, context)
    dst.write_el(model_name, res[0], function, res[1], -1, context=context)


def launch_models(model_names: List[str], src, dst):
    """
    Tests all models from model_names list from dataset src and writes results to dst dataset
    :param model_names: Usual List of LanguageModelName strings
    :param src: special object representing dataset (smth from datasets/database_utils)
    :param dst: special object representing dataset (smth from datasets/database_utils)
    :return: None
    """

    total_time = time.time()
    print_cyan("Starting testing models")

    for model_name in model_names:
        try:
            model = IdeLLM(model_name)

            cur_time = time.time()
            print_cyan(f"Testing model {model_name} now")

            dataset = src.get_data()
            for el in dataset:
                _get_model_prediction(model, model_name, dst, el[1], el[4])

            print_green(
                f"Finished testing model {model_name},"
                f" it took {round(time.time() - cur_time, 1)} seconds"
            )

        except BaseException as e:
            print_red(
                f"There was a mistake while processing model {model_name}"
            )

    print_green(
        f"Finished testing models,"
        f" it took {round(time.time() - total_time, 1)} seconds"
    )