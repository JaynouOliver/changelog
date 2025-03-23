import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

owner = os.getenv('OWNER')
repo = os.getenv('REPO')

github_token = os.getenv('GITHUB_API_KEY')


headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {github_token}",
    "X-GitHub-Api-Version": "2022-11-28"
}

def get_release_dates():
    try:
        release_url = f"https://api.github.com/repos/{owner}/{repo}/releases"
        getrequest = requests.get(release_url, headers=headers)
        getrequest.raise_for_status() #this is for raising an http error if it occurs 
        data = getrequest.json()
        # print(data)

        #extract the start and end dates
        get_date = [find["created_at"] for find in data]
        # print(f" debug {get_date}")
        # print(f" debug {get_date[0], get_date[1]}")

        start_date = get_date[0]
        end_date = get_date[1]
        return end_date, start_date

    except requests.exceptions.RequestException as e:
        print(f"error{e}")

def get_commits():
    try: 
        end_date, start_date = get_release_dates()
        commit_url = f"https://api.github.com/repos/{owner}/{repo}/commits?since={end_date}&until={start_date}&per_page=100&page=1"
        getrequest = requests.get(commit_url, headers=headers)
        getrequest.raise_for_status() #this is for raising an http error if it occurs 
        # print(getrequest.json())
        commits = [find["commit"]["message"] for find in getrequest.json()]
        commit_json = json.dumps(commits, indent=2) #send directly in json format
        return commit_json

    except requests.exceptions.RequestException as e:
        print(f"error{e}")
        return[]


from eval import analyze_commits
commit_data = get_commits()
analyze_commits(commit_data)