import requests
import os
import time

BASE_DIR = os.getenv('BASE_DIR')
# where you want to store the downloaded README files
readme_dir = os.path.join(BASE_DIR, 'readmes-update')

# Set the GITHUB_USERNAME and GITHUB_TOKEN environment variables
username = os.getenv('GITHUB_USERNAME')
token = os.getenv('GITHUB_TOKEN')

check_interval = 3600  # Check every hour
os.makedirs(readme_dir, exist_ok=True)

session = requests.Session()
session.auth = (username, token)

def get_starred_repos():
    url = f'https://api.github.com/users/{username}/starred'
    repos = []
    while url:
        response = session.get(url)
        response.raise_for_status()
        repos.extend(response.json())
        url = response.links.get('next', {}).get('url')
    return repos

def download_readme(repo):
    url = f"https://api.github.com/repos/{repo['owner']['login']}/{repo['name']}/readme"
    headers = {'Accept': 'application/vnd.github.v3.raw'}
    response = session.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None

def main():
    while True:
        print("Checking for new starred repositories...")
        repos = get_starred_repos()
        for repo in repos:
            readme_path = os.path.join(readme_dir, f"{repo['name']}_README.md")
            if not os.path.exists(readme_path):
                print(f"Downloading README for {repo['name']}")
                readme_content = download_readme(repo)
                if readme_content:
                    with open(readme_path, 'w', encoding='utf-8') as file:
                        file.write(readme_content)
            else:
                print(f"README for {repo['name']} already exists.")
        time.sleep(check_interval)

if __name__ == "__main__":
    main()
