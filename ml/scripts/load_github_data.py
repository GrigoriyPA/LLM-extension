import json
from os.path import expanduser

from tqdm import tqdm

from configs import database as database_config
from src import colourful_cmd
from src import database_entities
from src import database_utils
from src import github_searcher


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

dst_dataset = database_utils.Table(
    db=database_config.MAIN_DATABASE,
    table_name=database_config.GITHUB_DATA_TABLE,
    row_type=database_entities.Function
)

for repo in tqdm(config['repos']):
    author, repo_name = repo.split('/')
    data = github_searcher.get_functions_in_repo(
        author=author,
        repo=repo_name,
        context_wide=config['context_wide'],
        token=AUTHORIZATION_TOKEN,
        ignore_comments=config['ignore_comments'],
        ignore_tests=config['ignore_tests']
    )

    for row in data.values():
        dst_dataset.write(row)
