from fastapi import FastAPI

from backend.app.api.routes.chat import router as chat_router


app = FastAPI(
    title="Cura Customer Support API",
    version="1.0.0",
)

app.include_router(chat_router)


@app.get("/")
def root():
    return {
        "message": "Cura Customer Support API is running"
    }
