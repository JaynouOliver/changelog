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
        "Please analyze these commit messages and return a JSON as provided in the format mentioned in the pydantic model\n"
        "Commits:\n"
        f"{commit_data}"
    )
    response = get_chat_completion(instruction)
    # Clean response — handle Markdown or non-JSON outputs
    response = response.strip().strip("```").replace("json\n", "")

    try:
        parsed_response = OpenAIResponse.model_validate_json(response) #pydantic model
        print(parsed_response.model_dump_json(indent=2))
    except ValidationError as e:
        print("Validation Error:", e)
        print("Raw Response:", response)