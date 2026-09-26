import os
import time
from typing import List
from fastapi import FastAPI, Request, HTTPException, status
from pydantic import BaseModel, Field
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from prometheus_client import Counter, Histogram, make_asgi_app

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="MLOps Production Inference API", version="1.0.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

REQUEST_COUNT = Counter("prediction_requests_total", "Кількість запитів на інференс", ["model_version", "status"])
REQUEST_LATENCY = Histogram("prediction_latency_seconds", "Затримка інференсу в секундах", ["model_version"])

MODEL_VERSION = os.getenv("MODEL_VERSION", "v1.0.0")

class FeatureInput(BaseModel):
    features: List[float] = Field(
        ..., 
        min_length=4, 
        max_length=4, 
        description="Вектор рівно з 4 ознак (Iris dataset)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "features": [5.1, 3.5, 1.4, 0.2]
            }
        }

class PredictionResponse(BaseModel):
    model_version: str
    prediction: int
    latency: float

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "healthy", "model_version": MODEL_VERSION}

@app.get("/ready", status_code=status.HTTP_200_OK)
def readiness_check():
    return {"status": "ready"}

@app.post("/predict", response_model=PredictionResponse)
@limiter.limit("60/minute")
def predict(payload: FeatureInput, request: Request):
    start_time = time.time()
    try:
        features = payload.features
        # Базова логіка класифікації для Iris
        prediction = 0 if features[0] < 5.5 else (1 if features[2] < 4.8 else 2)
        latency = round(time.time() - start_time, 4)
        
        REQUEST_COUNT.labels(model_version=MODEL_VERSION, status="success").inc()
        REQUEST_LATENCY.labels(model_version=MODEL_VERSION).observe(latency)
        
        return PredictionResponse(
            model_version=MODEL_VERSION,
            prediction=prediction,
            latency=latency
        )
    except Exception as e:
        REQUEST_COUNT.labels(model_version=MODEL_VERSION, status="error").inc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
