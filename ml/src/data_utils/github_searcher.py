import base64
import collections
import time
import typing as tp
import json

import requests
from tqdm import tqdm

from src.data_utils import code_reader
from src.utils import colourful_cmd
from src.database import database_entities
from src.database import database_utils
from src.constants import github_searcher as github_searcher_constants


def get_headers(token):
    return {
            **github_searcher_constants.DEFAULT_HEADERS,
            "Authorization": f'Bearer {token}',
        }


def call_github_api(
        url: str,
        headers: tp.Dict[str, str]
) -> tp.Optional[requests.Response]:
    for _ in range(github_searcher_constants.API_TRY_COUNT):
        try:
            res = requests.get(
                url=url,
                headers=headers,
                timeout=github_searcher_constants.GITHUB_API_TIMEOUT,
            )
        except Exception as ex:
            colourful_cmd.print_red(
                f'Catch api error %s' % ex
            )
            time.sleep(github_searcher_constants.DELAY_TIME_SECONDS)
            continue
        return res
    return None


def get_all_python_files(
        author: str,
        repo: str,
        token: str,
) -> tp.List[str]:
    res = call_github_api(
        url=f'https://api.github.com/repos/'
            f'{author}/{repo}/git/trees/main?recursive=1',
        headers=get_headers(token=token)
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
        headers=get_headers(token=token)
    )
    if not res:
        return ''
    res = res.json()
    if 'content' not in res:
        return ''
    content = res['content']
    decoded = base64.b64decode(content).decode('utf-8')
    return decoded


def load_data_in_repo(
        author: str,
        repo: str,
        context_wide: int,
        token: str,
        ignore_comments: bool,
        ignore_tests: bool,
        functions_table: database_utils.Table,
        semantic_sense_table: database_utils.Table
) -> None:
    urls = get_all_python_files(
        author=author,
        repo=repo,
        token=token,
    )
    function_usages = collections.defaultdict(list)
    functions: tp.Dict[str, database_entities.Function] = {}
    tests: tp.Dict[str, database_entities.Function] = {}
    for url in (pbar := tqdm(urls)):
        pbar.set_description(f"Processing {url}")
        content = get_file_content(get_url=url, token=token)
        for name, code, docstring, variable in code_reader.get_functions_sources(
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
            if variable:
                semantic_sense_table.write(
                    database_entities.SemanticSense(
                        variable_name=variable,
                        context=code,
                    )
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
        for name, usage in code_reader.get_functions_calls(
                source_code=content,
                context_wide=context_wide
        ):
            if name in functions:
                function_usages[name].append(usage)
    for name in function_usages:
        functions[name].context = json.dumps(function_usages[name])
        functions_table.write(
            functions[name]
        )
