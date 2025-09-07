from fastapi import FastAPI, Request
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # For local testing

app = FastAPI()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # Private key

@app.post("/search")
async def search(request: Request):
    data = await request.json()
    query = data.get("query")
    if not query:
        return {"error": "No query provided."}

    url = "https://www.googleapis.com/customsearch/v1"
    params = {"key": GOOGLE_API_KEY, "cx": "YOUR_CUSTOM_SEARCH_ENGINE_ID", "q": query}
    response = requests.get(url, params=params)
    return response.json()
