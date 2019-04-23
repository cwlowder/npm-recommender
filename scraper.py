import json
import requests
import base64
import praw
import urllib

GITHUB_API_BASE = "https://api.github.com/"

def getGithubFileJson(user, repo, file):
    api_url = '{0}repos/{1}/{2}/contents/{3}'.format(GITHUB_API_BASE, user, repo, file)
    response = requests.get(api_url)

    if response.status_code is 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

def getGithubFileContent(user, repo, file):
    j = getGithubFileJson(user, repo, file)
    if j is not None:
        return base64.b64decode(j['content'])

if __name__ == "__main__":
    reddit = praw.Reddit()
    with open('reddit_all_github.txt', 'w') as file:
        for subreddit in reddit.subreddits.search('github'):
            for post in reddit.subreddit(subreddit.display_name).search('site:github.com', limit=10000):
                if not post.is_self and '://github.com' in post.url:
                    file.write('%s\n' % post.url)
    