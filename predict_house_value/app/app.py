from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from predict_house_value.db.database import engine

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



@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

