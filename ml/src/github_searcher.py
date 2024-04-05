import base64
import time

import requests
import src.code_reader as code_reader
import typing as tp

SEARCH_URL = 'https://api.github.com/search/code'


def search_files_with_definitions(
        author: str,
        repo: str,
        token: str,
) -> tp.List[str]:
    res = requests.get(
        url=SEARCH_URL + f'?q=def+in:file+language:python+repo:{author}/{repo}&type=code',
        headers={
            "Accept": "application/vnd.github.text-match+json",
            "Authorization": f'Bearer {token}',
            "X-GitHub-Api-Version": "2022-11-28"
        }
    )
    res = res.json()
    paths = {item['path']: item['git_url'] for item in res['items']}
    return list(paths.values())


def get_all_python_files(author: str, repo: str, token: str) -> tp.List[str]:
    res = requests.get(
        url=f'https://api.github.com/repos/{author}/{repo}/git/trees/main?recursive=1',
        headers={
            "Accept": "application/vnd.github.text-match+json",
            "Authorization": f'Bearer {token}',
            "X-GitHub-Api-Version": "2022-11-28"
        }
    )
    res = res.json()
    paths = [node['url'] for node in res['tree'] if node['path'][-3:] == '.py']
    return paths


def get_file_content(
        get_url: str,
        token,
) -> str:
    time.sleep(0.1)
    res = requests.get(
        url=get_url,
        headers={
            "Accept": "application/vnd.github.text-match+json",
            "Authorization": f'Bearer {token}',
            "X-GitHub-Api-Version": "2022-11-28"
        }
    ).json()
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
    for url in urls:
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
    for url in urls:
        content = get_file_content(get_url=url, token=token)
        for name, usage in code_reader.get_functions_calls(content, context_wide=context_wide):
            if name in data:
                data[name]['usages'].append(usage)
    return data
