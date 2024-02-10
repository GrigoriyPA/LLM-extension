import base64
import requests
import scripts.code_reader as code_reader
import time
import typing as tp


AUTHORIZATION_TOKEN = ''

SEARCH_URL = 'https://api.github.com/search/code'


def search_files_with_definitions(
        author: str,
        repo: str
) -> tp.List[str]:
    res = requests.get(
        url=SEARCH_URL + f'?q=def+in:file+language:python+repo:{author}/{repo}&type=code',
        headers={
            "Accept": "application/vnd.github.text-match+json",
            "Authorization": AUTHORIZATION_TOKEN,
            "X-GitHub-Api-Version": "2022-11-28"
        }
    )
    res = res.json()
    paths = {item['path']: item['git_url'] for item in res['items']}
    return list(paths.values())


def get_all_python_files(author: str, repo: str) -> tp.List[str]:
    res = requests.get(
        url=f'https://api.github.com/repos/'
            f'{author}/{repo}/git/trees/main?recursive=1',
        headers={
            "Accept": "application/vnd.github.text-match+json",
            "Authorization": AUTHORIZATION_TOKEN,
            "X-GitHub-Api-Version": "2022-11-28"
        }
    )
    time.sleep(0.01)
    res = res.json()
    paths = [node['url'] for node in res['tree'] if node['path'][-3:] == '.py']
    return paths


def get_file_content(
        get_url: str
) -> str:
    res = requests.get(
        url=get_url,
        headers={
            "Accept": "application/vnd.github.text-match+json",
            "Authorization": AUTHORIZATION_TOKEN,
            "X-GitHub-Api-Version": "2022-11-28"
        }
    ).json()
    time.sleep(0.01)
    if 'content' not in res:
        return ''
    content = res['content']
    decoded = base64.b64decode(content).decode('utf-8')
    return decoded


def get_functions_in_repo(
        author: str,
        repo: str
) -> tp.Dict[str, tp.Dict[str, tp.Any]]:
    urls = get_all_python_files(
        author=author,
        repo=repo
    )
    data = {}
    for url in urls:
        content = get_file_content(get_url=url)
        for name, code in code_reader.get_functions_sources(content):
            data[name] = {
                'name': name,
                'code': code,
                'usages': []
            }
        for name, usage in code_reader.get_functions_calls(content):
            if name in data:
                data[name]['usages'].append(usage)
    return data
