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
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": "Analyze the GitHub commit data. You already have knowledge about the code that is the commit messages. You have the knowledge of the industry. Try to understand what the organization is doing. Try to understand the commit messages. Try to understand what they are talking about. Combine information into categories. Categorize them accordingly in a proper JSON format as specified in the PYDANTIC structure. I want you to categorize them accordingly. MAKE THIS IN HUMAN READABLE FORMAT, FOR USERS WHO HAVE NO TECHNICAL KNOWLEDGE. Example  - you can simplify the bug fixes, simplify technical terms, and make it more appealing for to be presented in a customer facing website"},
                {"role": "user", "content": "\n".join(commits)},
            ],
            response_format=MainResponse,
        )

        event = completion.choices[0].message.parsed
        # event_json = json.dumps(event.model_dump(), indent=4) #converting to json format pydantic (https://docs.pydantic.dev/latest/concepts/serialization/) faced some problems here 🙃


        # print(event_json)
        return event
    except Exception as e:
        print(f"Error: {e}")
        return None
