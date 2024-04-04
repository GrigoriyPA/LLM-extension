import json
from src import github_searcher
from tqdm import tqdm
from src.colourful_cmd import print_cyan
from os.path import expanduser

from datasets.entities import Function
from datasets.database_utils import Dataset, Database
from datasets.datasets_config import CONTEXT_USAGES_SPLITTER

# token generation: https://github.com/settings/tokens

with open('scripts/config.json') as f:
    config = json.load(f)

GITHUB_TOKEN_PATH = expanduser('~/.llm_hse/github_token')

try:
    with open(GITHUB_TOKEN_PATH, 'r') as file:
        AUTHORIZATION_TOKEN = file.read().strip()
except FileNotFoundError:
    print_cyan(f"You must specify you github api token in {GITHUB_TOKEN_PATH}")
    raise

dst_database = Database('data/github_data')
dst_dataset = Dataset(dst_database, 'default_github_functions', Function)

for repo in tqdm(config['repos']):
    author, repo_name = repo.split('/')
    print('token is', AUTHORIZATION_TOKEN)
    data = github_searcher.get_functions_in_repo(
        author=author,
        repo=repo_name,
        context_wide=config['context_wide'],
        token=AUTHORIZATION_TOKEN,
    )

    for func_name in tqdm(data):
        row = data[func_name]
        dst_dataset.write(Function(
            function_name=row['name'],
            code=row['code'],
            docstring=row['docstring'],
            context=CONTEXT_USAGES_SPLITTER.join(row['usages']),
        ))
