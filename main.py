from pathlib import Path
from typing import List

import joblib
import numpy as np
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field


app = FastAPI(
    title="FastAPI ML Model API on Azure",
    description="A deployment-ready FastAPI app serving a Machine Learning model.",
    version="1.0.0",
)


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "iris_model.joblib"

model_bundle = None
model = None
class_names = []
feature_names = []
model_accuracy = None

if MODEL_PATH.exists():
    model_bundle = joblib.load(MODEL_PATH)
    model = model_bundle["model"]
    class_names = model_bundle["class_names"]
    feature_names = model_bundle["feature_names"]
    model_accuracy = model_bundle["accuracy"]


class IrisInput(BaseModel):
    sepal_length: float = Field(..., gt=0, examples=[5.1])
    sepal_width: float = Field(..., gt=0, examples=[3.5])
    petal_length: float = Field(..., gt=0, examples=[1.4])
    petal_width: float = Field(..., gt=0, examples=[0.2])

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sepal_length": 5.1,
                    "sepal_width": 3.5,
                    "petal_length": 1.4,
                    "petal_width": 0.2,
                }
            ]
        }
    }


class PredictionResponse(BaseModel):
    prediction_number: int
    prediction_class: str
    probabilities: dict[str, float]


def check_model_loaded() -> None:
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model is not loaded. Make sure models/iris_model.joblib exists. Run: python train_model.py",
        )


def convert_input_to_array(data: IrisInput) -> np.ndarray:
    return np.array(
        [[
            data.sepal_length,
            data.sepal_width,
            data.petal_length,
            data.petal_width,
        ]]
    )


def predict_single(data: IrisInput) -> PredictionResponse:
    check_model_loaded()

    input_array = convert_input_to_array(data)

    prediction_number = int(model.predict(input_array)[0])
    prediction_class = class_names[prediction_number]

    prediction_probabilities = model.predict_proba(input_array)[0]

    probabilities = {
        class_names[index]: round(float(probability), 4)
        for index, probability in enumerate(prediction_probabilities)
    }

    return PredictionResponse(
        prediction_number=prediction_number,
        prediction_class=prediction_class,
        probabilities=probabilities,
    )


@app.get("/")
def home():
    return {
        "message": "FastAPI ML API is running.",
        "docs": "/docs",
        "health": "/health",
        "predict": "POST /predict",
    }


@app.get("/health")
def health_check():
    return {
        "status": "running",
        "model_loaded": model is not None,
    }


@app.get("/model-info")
def model_info():
    check_model_loaded()

    return {
        "model_type": type(model).__name__,
        "accuracy": round(float(model_accuracy), 4),
        "feature_names": feature_names,
        "class_names": class_names,
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(data: IrisInput):
    return predict_single(data)


@app.post("/predict-batch", response_model=List[PredictionResponse])
def predict_batch(rows: List[IrisInput]):
    check_model_loaded()

    if len(rows) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Input list cannot be empty.",
        )

    return [predict_single(row) for row in rows]
