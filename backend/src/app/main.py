from app.routers import users, tournaments, matches, bots, admin
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)


app.include_router(users.router)
app.include_router(tournaments.router)
app.include_router(matches.router)
app.include_router(bots.router)
app.include_router(admin.router)


@app.get("/")
def read_root():
    return Response("Server is running.")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
