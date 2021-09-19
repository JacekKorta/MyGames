from fastapi import FastAPI

from backend.routers.game import router as GameRouter

app = FastAPI()

app.include_router(GameRouter, tags=["Game"], prefix="/my-games")
