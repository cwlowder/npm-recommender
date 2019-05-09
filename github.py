import json
import requests
import base64
import praw
import urllib

from utils import _progBar, loadFile

GITHUB_API_BASE = "https://api.github.com/"
GITHUB_CLIENT_ID = "e28bb4573a920da2033a"
GITHUB_CLIENT_SECRET = "7b1b3c0f68c47db4aa0024b72b0e12a5e6944049"

def getGithubFileJson(user, repo, file):
    api_url = '{0}repos/{1}/{2}/contents/{3}?client_id={4}&client_secret={5}'.format(GITHUB_API_BASE, user, repo, file, GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET)
    response = requests.get(api_url)

    if response.status_code is 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

def getGithubFileContent(user, repo, file):
    j = getGithubFileJson(user, repo, file)
    if j is not None:
        return base64.b64decode(j['content']).decode('utf-8')
    else:
        return None

def scrapeRedditForGithub(print_progress=False):
    github_links = []
    reddit = praw.Reddit()
    print("Scraping reddit for GitHub links:")
    for subreddit in reddit.subreddits.search('github'):
        i = 0
        for post in reddit.subreddit(subreddit.display_name).search('site:github.com', limit=10000):
            if print_progress:
                _progBar(i, 10000)
                i += 1
            if not post.is_self and '://github.com' in post.url:
                github_links.append(post.url)
    return github_links

def convertAllGithubToPackages(all_github, print_progress=False):
    all_packages = []
    print("Extracting package files from GitHub links:")
    i = 0
    for url in all_github:
        path = urllib.parse.urlparse(url[:-1]).path.split('/')[1:]
        if len(path) > 1:
            if print_progress:
                _progBar(i, len(all_github))
                i += 1
            else:
                print('{0}/{1}'.format(path[0], path[1]))
            package_json = getGithubFileContent(path[0], path[1], 'package.json')
            if package_json is not None:
                all_packages.append(''.join(package_json.split()))
    return all_packages

if __name__ == "__main__":
    all_github = scrapeRedditForGithub()
    # all_github = loadFile("data/reddit_all_github.txt")

    all_packages = convertAllGithubToPackages(all_github, True)
    print(len(all_packages))

