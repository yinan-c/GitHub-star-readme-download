import requests
import os

# Set the GITHUB_USERNAME and GITHUB_TOKEN environment variables
username = os.environ['GITHUB_USERNAME']
token = os.environ['GITHUB_TOKEN']

session = requests.Session()
session.auth = (username, token)

def get_starred_repos(username):
    url = f'https://api.github.com/users/{username}/starred'
    repos = []
    while url:
        response = session.get(url)
        response.raise_for_status()
        repos.extend(response.json())
        url = response.links.get('next', {}).get('url')
    return repos

def download_readme(repo_full_name):
    url = f'https://api.github.com/repos/{repo_full_name}/readme'
    headers = {'Accept': 'application/vnd.github.v3.raw'}
    response = session.get(url, headers=headers)
    response.raise_for_status()
    return response.text

starred_repos = get_starred_repos(username)

readme_dir = 'readmes'
os.makedirs(readme_dir, exist_ok=True)

for repo in starred_repos:
    repo_name = repo['full_name']
    print(f'Downloading README for {repo_name}')
    try:
        readme_content = download_readme(repo_name)
        with open(os.path.join(readme_dir, f'{repo_name.replace("/", "_")}_README.md'), 'w', encoding='utf-8') as file:
            file.write(readme_content)
    except requests.HTTPError as e:
        print(f'Failed to download README for {repo_name}: {e}')

print('Finished downloading all README files.')

