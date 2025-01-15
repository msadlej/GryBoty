from app.routers import admin, tournaments, matches, users, bots, games
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Response
from app.config import settings
import uvicorn


app = FastAPI()
app.include_router(admin.router, tags=["admin"])
app.include_router(users.router, tags=["users"])
app.include_router(bots.router, tags=["bots"])
app.include_router(tournaments.router, tags=["tournaments"])
app.include_router(matches.router, tags=["matches"])
app.include_router(games.router, tags=["games"])

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
        "X-XSRF-TOKEN"
    ],
    expose_headers=["*"]
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
