import base64
import collections
import time
import typing as tp
import json

import requests
from tqdm import tqdm

from src import code_reader
from src import colourful_cmd
from src import database_entities
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
        ignore_tests: bool
) -> tp.Dict[str, database_entities.Function]:
    urls = get_all_python_files(
        author=author,
        repo=repo,
        token=token,
    )
    function_usages = collections.defaultdict(list)
    functions: tp.Dict[str, database_entities.Function] = {}
    tests: tp.Dict[str, database_entities.Function] = {}
    for url in tqdm(urls):
        content = get_file_content(get_url=url, token=token)
        for name, code, docstring in code_reader.get_functions_sources(
                content,
                ignore_comments=ignore_comments
        ):
            if code_reader.is_test(name):
                tests[name] = database_entities.Function(
                    function_name=name,
                    docstring=docstring,
                    code=code,
                )
            else:
                functions[name] = database_entities.Function(
                    function_name=name,
                    docstring=docstring,
                    code=code,
                )

    for test in tests.values():
        function_name = code_reader.get_function_name_by_test_name(
            test_name=test.function_name
        )
        if function_name in functions:
            functions[function_name].unit_test = test.code
            print("UnitTest was found!", function_name)
        if not ignore_tests:
            functions[test.function_name] = test

    for url in tqdm(urls):
        content = get_file_content(get_url=url, token=token)
        for name, usage in code_reader.get_functions_calls(content, context_wide=context_wide):
            if name in functions:
                function_usages[name].append(usage)
    for name in function_usages:
        functions[name].context = json.dumps(function_usages[name])
    return functions
