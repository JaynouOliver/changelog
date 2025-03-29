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

        #get release name
        release_name = [find["name"] for find in data]
        print(f" release names \n \n {release_name}")

        #extract the start and end dates
        get_date = [find["published_at"] for find in data]
        print(f" \n dates \n \n {get_date}")
        # print(f" start and end dates {get_date[0], get_date[1]}")

        start_date = get_date[0]
        print(f" start date {start_date}")
        end_date = get_date[1]
        print(f" end date {end_date}")
        print(f" latest release name {release_name[0]}")
        return end_date, start_date, release_name[0]

    except requests.exceptions.RequestException as e:
        print(f"error{e}")

def get_commits():
    try: 
        end_date, start_date, release_name = get_release_dates()
        commit_url = f"https://api.github.com/repos/{owner}/{repo}/commits?since={end_date}&until={start_date}&per_page=100&page=1"
        getrequest = requests.get(commit_url, headers=headers)
        getrequest.raise_for_status() #this is for raising an http error if it occurs 
        # print(getrequest.json())
        commits = [find["commit"]["message"] for find in getrequest.json()]
        commit_json = json.dumps(commits, indent=2) #send directly in json format
        print(f" commits that will be fed to LLMs \n {commit_json}")
        return commit_json, release_name

    except requests.exceptions.RequestException as e:
        print(f"error{e}")
        return[]

import json
import os

def openai_json():
    try:
        commits, release_name = get_commits()
        # json_analyze_commits /= analyze_commits(commits=commits)
        return analyze_commits(commits=commits, release_name=release_name).model_dump()
        
    except Exception as e:
        print(f"Error: {e}")
        return None

def update_changelog(new_data):
    changelog_file = 'frontend.json'
    
    if new_data is None:
        return
    
    existing_data = []
    
    if os.path.exists(changelog_file):
        try:
            with open(changelog_file, 'r') as file:
                # Check if file has content before loading
                if os.stat(changelog_file).st_size > 0:
                    existing_data = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            # Handle empty/corrupted files
            existing_data = []
    
    # Combine new and existing data (prepend instead of append)
    # combined_data = new_data + existing_data
    #isinstance checks if the new data is a list, else it packs it into a list
    combined_data = (new_data if isinstance(new_data, list) else [new_data]) + existing_data
    
    with open(changelog_file, 'w') as file:
        json.dump(combined_data, file, indent=2)


def main():
    new_data = openai_json()
    if new_data is not None:
        update_changelog(new_data)
        event_json = json.dumps(new_data, indent=2)
        print(event_json)
        print("Changelog updated successfully.")
    else:
        print("Failed to generate changelog.")

if __name__ == "__main__":
    main()