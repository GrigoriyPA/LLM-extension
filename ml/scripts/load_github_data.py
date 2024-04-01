import json
import pandas as pd
from src import github_searcher
from tqdm import tqdm

# token generation: https://github.com/settings/tokens

with open('scripts/config.json') as f:
    config = json.load(f)

if config['github_token'] == 'your_token':
    print('replace github token')
    exit()


for repo in tqdm(config['repos']):
    pd_data = pd.DataFrame(columns=['name', 'docstring', 'code', 'usages'])
    author, repo_name = repo.split('/')
    data = github_searcher.get_functions_in_repo(
        author=author,
        repo=repo_name,
        context_wide=config['context_wide'],
        token=config['github_token']
    )

    for func_name in tqdm(data):
        row = data[func_name]
        pd_data.loc[-1] = (row['name'], row['docstring'], row['code'], row['usages'])
        pd_data.index = pd_data.index + 1
    pd_data.to_csv(f'{config["data_path"]}/{author}_{repo_name}.csv')
