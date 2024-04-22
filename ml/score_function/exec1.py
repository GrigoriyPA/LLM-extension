import pandas as pd
import json
from models_names import GPTModelName, GPTProviderName
import asyncio
from score_function import GenerativeModel, ScoreFunction
from src.entities import Function, ScorerModelDocstringResult


from .consts import SCORE_FUNCTION, PROMPTS

provider_name = SCORE_FUNCTION["provider_name"]
model_name = SCORE_FUNCTION["model_name"]
prompts = PROMPTS

a = """
    Add files to a tar-zip bundle.

    Parameters
    ----------
    bundle : Bundle
        The bundle to add the files to.
    root : str
        The root directory of the files.
    alias : str
        The alias of the files.
    file_names : list of str
        The names of the files to add.

    Returns
    -------
    None

    Example
    -------
    >>> bundle = Bundle()
    >>> root = 'path/to/files'
    >>> alias = 'files'
    >>> file_names = ['file1.txt', 'file2.txt']
    >>> add_files(bundle, root, alias, file_names)
    """

b =     """
def add_files(bundle, root, alias, file_names):
    for file_name in file_names:
        file_alias = os.path.join(alias, file_name)
        print(f"  {file_name} --> {file_alias}")
        bundle.add(os.path.join(root, file_name), file_alias)
"""

async def main():
    for i, prompt in enumerate(prompts):
        score_function = ScoreFunction(prompt)
        await score_function.exec_one(a, b)



asyncio.run(main())



