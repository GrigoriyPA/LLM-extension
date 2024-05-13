import asyncio
from tqdm import tqdm

from configs import prompts
from src.constants import database as database_config
from src.database import database_entities, database_utils
from src.scorers.score_function import GenerativeModel
import time
import re
async def build_finetune_dataset():
    src_dataset = database_utils.Table(
        db=database_config.MAIN_DATABASE,
        table_name=database_config.GITHUB_DATA_TABLE,
        row_type=database_entities.Function
    )

    dst_dataset = database_utils.Table(
        db=database_config.MAIN_DATABASE,
        table_name=database_config.FINETUNE_DOCSTRING_DATASET,
        row_type=database_entities.Function,
    )

    funcs = src_dataset.read()
    model = GenerativeModel()

    for i, func in enumerate(tqdm(funcs)):
        if i >= 0:
            func.docstring = await model.get_model_response(prompts.DOCSTRING_PROMPT.format(**func.__dict__))
            match = re.search(r'"""\s*(.*?)\s*"""', func.docstring, re.DOTALL)
            if match is not None:
                func.docstring = match.group(1)
            else:
                func.docstring = None
            dst_dataset.write(func)
            time.sleep(3)


asyncio.run(build_finetune_dataset())
