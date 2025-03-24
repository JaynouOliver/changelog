from pydantic import BaseModel
from openai import OpenAI
import json

client = OpenAI()

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

class SubResponse(BaseModel):
    whats_new: str
    impact: str
    changes_description: str
    other_info: str
    
class MainResponse(BaseModel):
    new_features: list[SubResponse]
    bug_fixes: list[SubResponse]
    tests: list[SubResponse]
    documentation: list[SubResponse]
    others: list[SubResponse]

def analyze_commits(commits):
    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": "Extract and categorize commit messages into the given format."},
                {"role": "user", "content": "\n".join(commits)},
            ],
            response_format=MainResponse,
        )

        event = completion.choices[0].message.parsed
        event_json = json.dumps(event.model_dump(), indent=4)
        print(event_json)
    except Exception as e:
        print(f"Error: {e}")
        return None
