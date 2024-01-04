from sqlmodel import create_engine, Session
from predict_house_value.config.config import URLs

engine = create_engine(URLs.DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session
