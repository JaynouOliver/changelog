import openai
import os
import json
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Pydantic model for OpenAI response
class OpenAIResponse(BaseModel):
    heading: str
    description: str


def get_chat_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]

# Fake Commit messages
commits = [
    "Added login functionality",
    "Fixed bug in data pipeline",
    "Improved API response time"
]

# Convert commits to JSON for the prompt
commit_json = json.dumps(commits, indent=2)


instruction = (
    "Please analyze these commit messages and return a JSON with the following format:\n"
    '{ "heading": "Brief title", "description": "Detailed explanation" }\n\n'
    "Commits:\n"
    f"{commit_json}"
)

response = get_chat_completion(instruction)


try:
    parsed_response = OpenAIResponse.model_validate_json(response)
    print(parsed_response.model_dump_json(indent=2))
except ValidationError as e:
    print("Validation Error:", e)