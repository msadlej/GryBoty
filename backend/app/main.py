from fastapi import FastAPI, Response
from app.routers import users
import uvicorn


app = FastAPI()
app.include_router(users.router)


@app.get("/")
def read_root():
    return Response("Server is running.")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
