from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
load_dotenv(find_dotenv())

from fastapi import FastAPI, Response, Query
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes

from functions.chat_history import _per_request_config_modifier
from chains.base_chain import chain_with_history
from models.response_models import CookieResponse


app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="Spin up a simple api server using Langchain's Runnable interfaces",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


add_routes(
    app,
    chain_with_history,
    per_req_config_modifier=_per_request_config_modifier,
    # Disable playground and batch
    # 1) Playground we're passing information via headers, which is not supported via
    #    the playground right now.
    # 2) Disable batch to avoid users being confused. Batch will work fine
    #    as long as users invoke it with multiple configs appropriately, but
    #    without validation users are likely going to forget to do that.
    #    In addition, there's likely little sense in support batch for a chatbot.
    disabled_endpoints=["playground", "batch"],
    path="/base"
)


# APIs for setting the user_id cookie in the Swagger UI
@app.get("/set-cookie/", response_model=CookieResponse)
async def set_cookie(
    user_id: str = Query(..., description="The value of the user_id cookie"),
    response: Response = None
) -> CookieResponse:
    # Set a cookie with the provided key and value
    response.set_cookie(key="user_id", value=user_id)
    return {"message": "user_id cookie set!", "value": user_id}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
