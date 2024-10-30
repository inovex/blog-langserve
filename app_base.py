from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
load_dotenv(find_dotenv())

from fastapi import FastAPI
from langchain_openai import AzureChatOpenAI
from langserve import add_routes

import uvicorn


app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="LangChain API Server"
)

add_routes(
    app,
    AzureChatOpenAI(deployment_name="gpt-4-turbo"),
    path="/openai"
)

if __name__=="__main__":
    uvicorn.run(app, host="localhost", port=8000)
