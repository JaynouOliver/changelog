import os
import requests
import json
from dotenv import load_dotenv
from response import analyze_commits

load_dotenv()

owner = os.getenv('OWNER')
repo = os.getenv('REPO')

github_token = os.getenv('API_KEY_GITHUB')


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
        get_date = [find["published_at"] for find in data]
        print(f" dates \n {get_date}")
        print(f" start and end dates {get_date[0], get_date[1]}")

        start_date = get_date[0]
        print(f" start date {start_date}")
        end_date = get_date[1]
        print(f" end date {end_date}")
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
        print(f" commits that will be fed to LLMs \n {commit_json}")
        return commit_json

    except requests.exceptions.RequestException as e:
        print(f"error{e}")
        return[]

import json
import os

def openai_json():
    try:
        commits = get_commits()
        # json_analyze_commits /= analyze_commits(commits=commits)
        return analyze_commits(commits=commits).model_dump()
        
    except Exception as e:
        print(f"Error: {e}")
        return None

def update_changelog(new_data):
    changelog_file = 'changelog.json'
    
    try:
        if new_data is None:
            return
        
        if os.path.exists(changelog_file) and os.path.getsize(changelog_file) > 0:
            with open(changelog_file, 'r') as file:
                try:
                    existing_data = json.load(file)
                except json.JSONDecodeError:
                    # If JSON is invalid, start fresh with empty list
                    existing_data = []
        else:
            existing_data = []
        
        # Ensure new_data is a list
        if not isinstance(new_data, list):
            new_data = [new_data]
        
        # Combine new and existing data (prepend instead of append)
        combined_data = new_data + existing_data
        
        with open(changelog_file, 'w') as file:
            json.dump(combined_data, file, indent=2)
            
    except Exception as e:
        print(f"Error: {e}")

def main():
    new_data = openai_json()
    if new_data is not None:
        update_changelog(new_data)
        print("Changelog updated successfully.")
    else:
        print("Failed to generate changelog.")

if __name__ == "__main__":
    main()
