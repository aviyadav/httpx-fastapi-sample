from asyncio import timeout
from http.client import responses

from fastapi import FastAPI
from httpx import AsyncClient, Timeout

app = FastAPI()
timeout = Timeout(10.0, connect=5.0)

@app.on_event("startup")
async def startup_event():
    app.state.http_client = AsyncClient(http2=True, timeout=timeout)

@app.on_event("shutdown")
async def shutdown_event():
    await app.state.http_client.aclose()

@app.get("/")
async def get_root():
    return {"Hello": "World"}

@app.get("/data")
async def get_data():
    async with app.state.http_client as client:
        response = await client.get("http://localhost:9900/") # any url that returns json data
        return response.json()