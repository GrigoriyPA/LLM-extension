import json
from os.path import expanduser

from tqdm import tqdm

from src.constants import database as database_config
from src.utils import colourful_cmd
from src.database import database_entities, database_utils
from src.data_utils import github_searcher

# token generation: https://github.com/settings/tokens

with open('scripts/config.json') as f:
    config = json.load(f)

GITHUB_TOKEN_PATH = expanduser(config['github_token_path'])

try:
    with open(GITHUB_TOKEN_PATH, 'r') as file:
        AUTHORIZATION_TOKEN = file.read().strip()
except FileNotFoundError:
    colourful_cmd.print_cyan(
        f"You must specify you github api token in {GITHUB_TOKEN_PATH}"
    )
    raise

functions_table = database_utils.Table(
    db=database_config.MAIN_DATABASE,
    table_name=database_config.GITHUB_DATA_TABLE,
    row_type=database_entities.Function
)


semantic_sense_table = database_utils.Table(
    db=database_config.MAIN_DATABASE,
    table_name=database_config.GITHUB_DATA_VARIABLES_TABLE,
    row_type=database_entities.SemanticSense
)

for repo in (pbar := tqdm(config['repos'])):
    pbar.set_description(repo)
    author, repo_name = repo.split('/')
    github_searcher.load_data_in_repo(
        author=author,
        repo=repo_name,
        context_wide=config['context_wide'],
        token=AUTHORIZATION_TOKEN,
        ignore_comments=config['ignore_comments'],
        ignore_tests=config['ignore_tests'],
        functions_table=functions_table,
        semantic_sense_table=semantic_sense_table
    )
