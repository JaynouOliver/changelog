from fastapi import FastAPI
from main import openai_json 

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/openai")
async def read_item():

    try:
        answer  = openai_json()
        return answer
    except Exception as e:
        return str(e)
        