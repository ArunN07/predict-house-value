from typing import Dict
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from predict_house_value.db.database import get_session
from predict_house_value.app.schema import TrainingData
from sqlmodel import Session
from sqlalchemy.exc import IntegrityError

router = APIRouter()


def add_training_data_to_db(db: Session, training_data: Dict[str], input_file: UploadFile):
    db_training_data = TrainingData(**training_data, input_file_name=input_file.filename)
    db.add(db_training_data)
    db.commit()
    db.refresh(db_training_data)
    return db_training_data


@router.post("/upload-training-data/")
async def upload_training_data(
    training_data: Dict[str],
    input_file: UploadFile = File(...),
    db: Session = Depends(get_session)
):
    try:
        db_training_data = add_training_data_to_db(db, training_data, input_file)
        return JSONResponse(content={"message": "Training data uploaded successfully"}, status_code=201)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Duplicate entry. Training data already exists.") from e
    except Exception as e:
        raise HTTPException(status_code=400, detail="Other database error.") from e

