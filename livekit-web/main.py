import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from livekit import api

LIVEKIT_URL = os.environ["LIVEKIT_URL"]
LIVEKIT_API_KEY = os.environ["LIVEKIT_API_KEY"]
LIVEKIT_API_SECRET = os.environ["LIVEKIT_API_SECRET"]

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # render HTML viewer
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "livekit_url": LIVEKIT_URL}
    )


@app.get("/token")
async def token(identity: str, room: str):
    # server-side mint token (secret stays on server)
    at = api.AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)\
        .with_identity(identity)\
        .with_name(identity)

    at.with_grants(api.VideoGrants(room_join=True, room=room))

    return {"token": at.to_jwt(), "url": LIVEKIT_URL}
