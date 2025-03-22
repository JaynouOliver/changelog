import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

owner = os.getenv('OWNER')
repo = os.getenv('REPO')

github_token = os.getenv('GITHUB_API_KEY')

release_url = f"https://api.github.com/repos/{owner}/{repo}/releases"


headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {github_token}",
    "X-GitHub-Api-Version": "2022-11-28"
}

def get_release_dates():
    try:
        getrequest = requests.get(release_url, headers=headers)
        getrequest.raise_for_status #this is for raising an http error if it occurs 
        data = getrequest.json()
        # print(data)

        #extract the start and end dates
        get_date = [find["created_at"] for find in data]
        # print(f" debug {get_date}")
        # print(f" debug {get_date[0], get_date[1]}")
        return get_date[0], get_date[1]

    except requests.exceptions.RequestException as e:
        print(f"error{e}")



# call_function = get_release_dates()
# print(call_function)

# start_date, end_date = call_function
# print(f"{start_date} \n {end_date}")




commit_url = f"https://api.github.com/repos/{owner}/{repo}/commits?since=2025-03-18T11:15:09Z&until=2025-03-21T13:25:38Z&per_page=100&page=1"

def get_commits():
    try:
        getrequest = requests.get(commit_url, headers=headers)
        getrequest.raise_for_status() #this is for raising an http error if it occurs 
        data = getrequest.json()
        # print(data)

        get_commit = [find["commit"]["message"] for find in data]
        return get_commit

    except requests.exceptions.RequestException as e:
        print(f"error{e}")

call_func = get_commits()
json_data = json.dumps(call_func, indent=6)
print(json_data)


