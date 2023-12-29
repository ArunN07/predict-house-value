from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from predict_house_value.app.routers.prediction_router import prediction_router
from predict_house_value.db.database import engine
import uvicorn

app = FastAPI(
    title="Your Project Name",
    version="1.0",
    description="Your project description",
    contact={"name": "Your Name", "email": "your.email@example.com"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prediction_router)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    uvicorn.run("app:app", reload=True, port=8002)

