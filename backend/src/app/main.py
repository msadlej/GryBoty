from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Response
import uvicorn

from app.routers import admin, users, bots, tournaments, matches, game_types
from app.config import settings


app = FastAPI()
app.include_router(admin.router, tags=["admin"])
app.include_router(users.router, tags=["users"])
app.include_router(bots.router, tags=["bots"])
app.include_router(tournaments.router, tags=["tournaments"])
app.include_router(matches.router, tags=["matches"])
app.include_router(game_types.router, tags=["game_types"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "Accept",
        "Origin",
        "X-XSRF-TOKEN",
    ],
    expose_headers=["*"],
)


@app.get("/")
def read_root():
    return Response("Server is running.")


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=(settings.ENVIRONMENT == "local"),
    )
