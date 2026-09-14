from fastapi import FastAPI

from app.routers import auth, gmail

app = FastAPI()
app.include_router(auth.router)
app.include_router(gmail.router)


@app.get("/")
def health_check():
    return {"status": "ok"}
