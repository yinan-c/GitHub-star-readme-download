import requests
import feedparser
import time
import os

BASE_DIR = os.getenv('BASE_DIR')
# where you want to store the downloaded README files
FEED_URL = os.getenv('FEED_URL')
# example FEED_URL = 'https://your_rsshub.app/github/stars/your_username'

README_DIR = os.path.join(BASE_DIR, 'readmes-rss')
DOWNLOAD_LOG = os.path.join(BASE_DIR, 'downloaded_log.txt')
CHECK_INTERVAL = 3600
os.makedirs(README_DIR, exist_ok=True)

if not os.path.exists(DOWNLOAD_LOG):
    with open(DOWNLOAD_LOG, 'w') as f:
        pass

def read_downloaded_log():
    with open(DOWNLOAD_LOG, 'r') as file:
        downloaded = file.read().splitlines()
    return downloaded

def write_downloaded_log(repo_name):
    with open(DOWNLOAD_LOG, 'a') as file:
        file.write(repo_name + '\n')

def download_readme(repo_url):
    api_url = f'https://api.github.com/repos/{repo_url.split("/")[-2]}/{repo_url.split("/")[-1]}/readme'
    headers = {'Accept': 'application/vnd.github.v3.raw'}
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None

def main():
    downloaded_repos = read_downloaded_log()
    while True:
        print("Checking for new starred repositories...")
        feed = feedparser.parse(FEED_URL)
      #  print(feed.entries)
        new_entries = [entry for entry in feed.entries if entry.link not in downloaded_repos]
        print(f"Found {len(new_entries)} new repositories.")
        for entry in new_entries:
            print(f"New repository found: {entry.title}")
            readme_content = download_readme(entry.link)
            if readme_content:
                filename = f'{entry.title.replace("/", "_")}_README.md'
                with open(os.path.join(README_DIR, filename), 'w', encoding='utf-8') as file:
                    file.write(readme_content)
                write_downloaded_log(entry.link)
                print(f"Downloaded README for {entry.title}")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
