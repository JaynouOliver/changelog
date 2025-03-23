import os
import requests
import json
from dotenv import load_dotenv
from eval import ai_response

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

        start_date = get_date[0]
        end_date = get_date[1]
        return end_date, start_date

    except requests.exceptions.RequestException as e:
        print(f"error{e}")

def get_commits(end_date, start_date):
    try: 
        
        commit_url = f"https://api.github.com/repos/{owner}/{repo}/commits?since={end_date}&until={start_date}&per_page=100&page=1"
        getrequest = requests.get(commit_url, headers=headers)
        getrequest.raise_for_status() #this is for raising an http error if it occurs 
        # print(getrequest.json())
        commits = [find["commit"]["message"] for find in getrequest.json()]
        return commits

    except requests.exceptions.RequestException as e:
        print(f"error{e}")
        return[]


if __name__ == "__main__":
    start_date, end_date = get_release_dates()
    print(f"Fetching commits between:\n{start_date} (start)\n{end_date} (end)")
    
    commits = get_commits(start_date, end_date)
    # print(json.dumps(commits, indent=2))


# data = ai_response(commits=commits)
# print(data)

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

def ai_response(commits: list[str]):
    try:
        client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        )

        completion = client.chat.completions.create(
        #   extra_headers={
        #     "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
        #     "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
        #   },
        extra_body={},
        model="deepseek/deepseek-r1-zero:free",
        messages=[
            {
            "role": "user",
            "content": "What is the meaning of life?"
            }
        ]
        )
        print(completion.choices[0].message.content)
    except requests.exceptions.RequestException as e:
        print(f"error{e}")




