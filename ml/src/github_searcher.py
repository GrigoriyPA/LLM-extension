import base64
import time
import typing as tp

import requests
from tqdm import tqdm

from src import code_reader
from src import colourful_cmd
from constants import github_searcher as github_searcher_constants

SEARCH_URL = 'https://api.github.com/search/code'


def call_github_api(
        url: str,
        headers: tp.Dict[str, str]
) -> tp.Optional[requests.Response]:
    for _ in range(github_searcher_constants.API_TRY_COUNT):
        try:
            res = requests.get(
                url=url,
                headers=headers
            )
        except Exception as ex:
            colourful_cmd.print_red(
                f'Catch api error %s' % ex
            )
            time.sleep(github_searcher_constants.DELAY_TIME_SECONDS)
            continue
        return res
    return None


def search_files_with_definitions(
        author: str,
        repo: str,
        token: str,
) -> tp.List[str]:
    res = call_github_api(
        url=(
            SEARCH_URL
            + f'?q=def+in:file+language:python+repo:{author}/{repo}&type=code'
        ),
        headers={
            **github_searcher_constants.DEFAULT_HEADERS,
            "Authorization": f'Bearer {token}',
        }
    )
    if not res:
        return []
    res = res.json()
    paths = {item['path']: item['git_url'] for item in res['items']}
    return list(paths.values())


def get_all_python_files(
        author: str,
        repo: str,
        token: str,
) -> tp.List[str]:
    res = call_github_api(
        url=f'https://api.github.com/repos/'
            f'{author}/{repo}/git/trees/main?recursive=1',
        headers={
            **github_searcher_constants.DEFAULT_HEADERS,
            "Authorization": f'Bearer {token}',
        }
    )
    if not res:
        return []
    res = res.json()
    paths = [node['url'] for node in res['tree'] if node['path'][-3:] == '.py']
    return paths


def get_file_content(
        get_url: str,
        token,
) -> str:
    res = call_github_api(
        url=get_url,
        headers={
            **github_searcher_constants.DEFAULT_HEADERS,
            "Authorization": f'Bearer {token}',
        }
    )
    if not res:
        return ''
    res = res.json()
    if 'content' not in res:
        return ''
    content = res['content']
    decoded = base64.b64decode(content).decode('utf-8')
    return decoded


def get_functions_in_repo(
        author: str,
        repo: str,
        context_wide: int,
        token: str,
        ignore_comments: bool,
) -> tp.Dict[str, tp.Dict[str, tp.Any]]:
    urls = get_all_python_files(
        author=author,
        repo=repo,
        token=token,
    )
    data = {}
    for url in tqdm(urls):
        content = get_file_content(get_url=url, token=token)
        for name, code, docstring in code_reader.get_functions_sources(
                content,
                ignore_comments=ignore_comments
        ):
            data[name] = {
                'name': name,
                'docstring': docstring,
                'code': code,
                'usages': []
            }
    for url in tqdm(urls):
        content = get_file_content(get_url=url, token=token)
        for name, usage in code_reader.get_functions_calls(content, context_wide=context_wide):
            if name in data:
                data[name]['usages'].append(usage)
    return data
