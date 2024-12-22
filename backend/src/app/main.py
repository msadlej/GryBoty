from app.routers import admin, tournaments, matches, users, bots, games
from app.config import settings
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


app = FastAPI()
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(tournaments.router)
app.include_router(matches.router)
app.include_router(bots.router)
app.include_router(games.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return Response("Server is running.")


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=(settings.ENVIRONMENT == "local"),
    )
