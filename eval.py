from typing_extensions import Optional
import openai
import os
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError
from typing import List, Optional
import re

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


class ChangeItem(BaseModel):
    whats_new: str
    impact: Optional[str] = None
    changes_description: str
    other_info: Optional[str] = None

class OpenAIResponse(BaseModel):
    new_features: List[ChangeItem]
    bug_fixes: List[ChangeItem]
    tests: List[ChangeItem]
    documentation: List[ChangeItem]
    others: List[ChangeItem]


#openai function
def get_chat_completion(prompt, model="gpt-4o"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]

def analyze_commits(commit_data):
    instruction = (
    "Respond only with the JSON in the format provided. Do not include any explanatory text or introduction."
    "You’re a changelog generator for a consumer-facing website. Your job is to analyze commit messages, extract meaningful insights, and present them in clear categories. Focus on summarizing changes, merging related commits, and avoiding technical jargon when possible.\n\n"
    "Categorize changes into these groups:\n"
    "1. New Features: Any new functionality added.\n"
    "2. Bug Fixes: Resolved issues and bugs.\n"
    "3. Tests: Changes related to testing.\n"
    "4. Documentation: Updates to docs or comments.\n"
    "5. Others: Anything that doesn't fit in the above.\n\n"
    "For each group, combine related commits into a single entry when appropriate. Avoid repeating commit messages verbatim — instead, summarize them. Provide a high-level overview in simple terms.\n\n"
    "Example:\n"
    "Raw Commits:\n"
    "- Fix: dtype cannot be str (#36262)\n"
    "- Minor Gemma 3 fixes  (#36884)\n\n"
    "Expected Output:\n"
    "\"bug_fixes\": {\n"
    "   \"whats_new\": \"Fixed issues with data type handling in Gemma 3.\",\n"
    "   \"impact\": \"Prevents runtime errors in edge cases.\",\n"
    "   \"changes_description\": \"Resolved dtype mismatch and improved Gemma 3 model handling.\",\n"
    "   \"other_info\": null\n"
    "}\n\n"
    "Commits:\n"
    f"{commit_data}"
)
    response = get_chat_completion(instruction)
    # Extract the JSON part using regex
    # match = re.search(r'```json\n(.*?)\n```', response, re.S)
    # if match:
    #     json_text = match.group(1)
    # else:
    #     # Try parsing directly in case there's no markdown
    #     json_text = response.strip()

    try:
        parsed_response = OpenAIResponse.model_validate_json(response) #pydantic model
        print(parsed_response.model_dump_json(indent=2))
    except ValidationError as e:
        print("Validation Error:", e)
        print("Raw Response:", response)